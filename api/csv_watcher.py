import logging
import os
import time
from dataclasses import dataclass
from os.path import join
from typing import List

import pandas as pd
from threading import Thread
import glob

from database import DatabaseClient
from database.client import COLS


@dataclass
class CSVFilepathForTable:
    filepath: str
    table: str


class CSVWatcher(Thread):
    """
    Looks for csv files that contains historic data, in order to load and store it into the database.
    """

    def __init__(self, csv_directory_path: str, client: DatabaseClient):
        super().__init__()
        self.active = True
        self.csv_directory_path = csv_directory_path
        self.client = client
        self.filename_key_to_table_name = {
            "hired_employees.csv": "employees",
            "departments.csv": "departments",
            "jobs.csv": "jobs"
        }  # this map is used to tell the CSVWatcher that data from a csv file has to be inserted in certain table.
        # For ex: csv files that contain rows for 'employees' table, must be mamed 'hired_employees.csv'.

    def _look_for_csv(self) -> List[CSVFilepathForTable]:
        """
        Inspects the folder where csv files are located and return a list of CSVFilepathForTable: objects that stores
        a filepath and its associated db table.
        :return: List[CSVFilepathForTable]
        """
        file2table_list = []
        filenames_keys = self.filename_key_to_table_name.keys()
        for filepath in glob.glob(join(self.csv_directory_path, "*.csv")):
            filename = filepath.split('/')[-1]
            if not filename in filenames_keys:
                logging.error(f"File {filename} is not named as {list(filenames_keys)}. Will be ignored.")
                continue
            f2table = CSVFilepathForTable(filepath, self.filename_key_to_table_name[filename])
            file2table_list.append(f2table)
            logging.info(f"Founded file in {f2table.filepath} that contains data for table {f2table.table}")

        return file2table_list

    def _insert_to_db(self, filep2table: List[CSVFilepathForTable]) -> None:
        """
        Reads the csv files, by chunks, and uses the DatabaseClient to store data in tables.
        :param filep2table: A list of CSVFilepathForTable objects.
        :return:
        """
        for ft in filep2table:
            cols = COLS[ft.table]
            for inx, chunk in enumerate(pd.read_csv(ft.filepath, names=cols,
                                                    chunksize=100000,
                                                    infer_datetime_format=True)):  # csv files may be too big, so I read it in
                # chunks.
                chunk = chunk.dropna()
                if "datetime" in cols:
                    chunk["datetime"] = pd.to_datetime(chunk["datetime"])

                objects = list(map(lambda r: {col: field for col, field in zip(cols, r)}, chunk.values))
                logging.info(f"Inserting new rows into table {ft.table}. Chunk {inx}.")
                self.client.insert_to(table=ft.table, objects=objects)
                logging.info("Done!")

    @staticmethod
    def _rename_csv(filep2table: List[CSVFilepathForTable]) -> None:
        """
        Rename csv files in order to be ignored later by Worker.
        :param filep2table: A list of CSVFilepathForTable objects.
        :return: None
        """
        for ft in filep2table:
            filepath = ft.filepath
            filename = os.path.basename(filepath)
            new_filepath = join(os.path.dirname(filepath), "LOAED_" + filename)
            os.rename(filepath, new_filepath)

    def run(self) -> None:
        while self.active:
            logging.info("Looking for csv data...")
            file2table_list = self._look_for_csv()
            if len(file2table_list) > 0:
                logging.info("New historic data founded!")
                logging.info(f"{file2table_list}")
            self._insert_to_db(file2table_list)
            self._rename_csv(file2table_list)
            time.sleep(10)

        logging.warning("CSVWatcher not looking for historic data anymore.")
