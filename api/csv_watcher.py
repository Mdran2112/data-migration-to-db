import logging
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
        self.csv_directory_path = csv_directory_path
        self.client = client
        self.filename_key_to_table_name = {
            "hired_employees.csv": "employees",
            "departments.csv": "departments",
            "jobs.csv": "jobs"
        }  # this map is used to tell the CSVWatcher that data from a csv file has to be inserted in certain table.
        # For ex: csv files that contain rows for 'employees' table, must be mamed 'hired_employees.csv'.

    def _look_for_csv(self) -> List[CSVFilepathForTable]:
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
        for ft in filep2table:
            cols = COLS[ft.table]
            for chunk in pd.read_csv(ft.filepath, chunksize=100000):
                objects = list(map(lambda r: {col: field for col, field in zip(cols, r)}, chunk.values))
                logging.info(f"Inserting new rows into table {ft.table}")
                self.client.insert_to(table=ft.table, objects=objects)

