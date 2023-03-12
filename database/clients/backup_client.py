import json
import logging
import os
from os.path import join
from typing import Dict, List, Any

import avro
from avro.datafile import DataFileWriter
from avro.io import DatumWriter
from sqlalchemy.orm import Session

from database import Base
from database.models import Employee, Department, Job, EMPLOYEES_TABLE, DEPARTMENT_TABLE, \
    JOB_TABLE, EMPLOYEE_COLS, DEPARTMENT_COLS, JOB_COLS
from database.models.avro.schemas import EMPLOYEE_SCHEMA, DEPARTMENT_SCHEMA, JOB_SCHEMA
from globals import BACKUP_DIRECTORY_PATH


class BackUpClient:
    """
    client used for getting tables from the database. It will get all the available data from
    certain table and store it in avro format.
    Attributes
    ----------
    session: Session
       SQLAlchemy session.
    """

    CHUNK_SIZE = int(os.getenv("BACK_UP_CHUNK_SIZE", 100000))

    def __init__(self, session: Session) -> None:
        self._session = session

    def _to_avro(self, mapper: Base,
                 schema: Dict[str, Any],
                 cols: List[str],
                 filename: str):

        schema_obj = avro.schema.parse(json.dumps(schema))
        writer = DataFileWriter(open(filename, "wb"), DatumWriter(), schema_obj)

        res = self._session.execute(mapper.__table__.select())
        while True:
            try:
                chunk = res.fetchmany(self.CHUNK_SIZE)
            except Exception as ex:
                self._session.rollback()
                raise ex
            if not chunk:
                break
            for obj in chunk:
                writer.append({col: value.strftime("%Y-%m-%dT%H:%M:%S") if col == "datetime" else value for col, value
                               in zip(cols, obj)})
        writer.close()
        target_filename = filename.replace("_temp", "")

        if os.path.exists(target_filename):
            os.remove(target_filename)
        os.rename(filename, target_filename)
        logging.info(f"Done! Backup has been stored in {target_filename}")

    def _employees_to_avro(self):
        logging.info("Getting rows from Employees table...")
        self._to_avro(mapper=Employee, schema=EMPLOYEE_SCHEMA,
                      cols=EMPLOYEE_COLS, filename=join(BACKUP_DIRECTORY_PATH, f"{EMPLOYEES_TABLE}_temp.avro"))

    def _departments_to_avro(self):
        logging.info("Getting rows from Departments table...")
        self._to_avro(mapper=Department, schema=DEPARTMENT_SCHEMA,
                      cols=DEPARTMENT_COLS, filename=join(BACKUP_DIRECTORY_PATH, f"{DEPARTMENT_TABLE}_temp.avro"))

    def _jobs_to_avro(self):
        logging.info("Getting rows from Jobs table...")
        self._to_avro(mapper=Job, schema=JOB_SCHEMA,
                      cols=JOB_COLS, filename=join(BACKUP_DIRECTORY_PATH, f"{JOB_TABLE}_temp.avro"))

    def build_backup_for(self, table: str) -> None:

        if table == EMPLOYEES_TABLE:
            self._employees_to_avro()
        elif table == DEPARTMENT_TABLE:
            self._departments_to_avro()
        elif table == JOB_TABLE:
            self._jobs_to_avro()
