import logging
from typing import List, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import Base
from database.models import Employee, Department, Job, EMPLOYEES_TABLE, DEPARTMENT_TABLE, \
    JOB_TABLE, EMPLOYEE_COLS, DEPARTMENT_COLS, JOB_COLS

COLS = {
    EMPLOYEES_TABLE: EMPLOYEE_COLS,
    DEPARTMENT_TABLE: DEPARTMENT_COLS,
    JOB_TABLE: JOB_COLS
}


class DatabaseClient:
    """
    client used for interacting with database.
    Attributes
    ----------
    session: Session
       SQLAlchemy session.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def _insert(self, mapper: Base, objects: List[Dict[str, Any]]):
        len_o = len(objects)
        if len_o == 0:
            raise ValueError("None of the objects could be inserted, maybe because all of them didn't satisfied the "
                             "Data Rules.")
        try:
            logging.info(f"{len_o} will be inserted.")
            self._session.bulk_insert_mappings(mapper=mapper, mappings=objects)
            self.session_commit()
        except Exception as ex:
            self._session.rollback()
            raise ex

    def insert_employees(self, objects: List[Dict[str, Any]]) -> None:
        self._insert(mapper=Employee, objects=objects)

    def insert_departments(self, objects: List[Dict[str, Any]]) -> None:
        self._insert(mapper=Department, objects=objects)

    def insert_jobs(self, objects: List[Dict[str, Any]]) -> None:
        self._insert(mapper=Job, objects=objects)

    def insert_to(self, table: str, objects: List[Dict[str, Any]]) -> None:

        if table == EMPLOYEES_TABLE:
            self.insert_employees(objects)
        elif table == DEPARTMENT_TABLE:
            self.insert_departments(objects)
        elif table == JOB_TABLE:
            self.insert_jobs(objects)

    def session_commit(self) -> None:
        self._session.commit()
