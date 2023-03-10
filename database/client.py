import logging
from datetime import date
from functools import wraps
from typing import List, Dict, Any, Tuple

from pymysql import ProgrammingError
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import Employee, Department, Job, EMPLOYEES_TABLE, DEPARTMENT_TABLE, \
    JOB_TABLE, EMPLOYEE_COLS, DEPARTMENT_COLS, JOB_COLS

COLS = {
    EMPLOYEES_TABLE: EMPLOYEE_COLS,
    DEPARTMENT_TABLE: DEPARTMENT_COLS,
    JOB_TABLE: JOB_COLS
}


def handle_error(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        try:
            resp = f(*args, **kws)
            return resp
        except Exception as ex:
            logging.error(str(ex))

    return decorated_function


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

    @handle_error
    def insert_employees(self, objects: List[Dict[str, Any]]) -> None:
        self._session.bulk_insert_mappings(mapper=Employee, mappings=objects)
        self.session_commit()

    @handle_error
    def insert_departments(self, objects: List[Dict[str, Any]]) -> None:
        self._session.bulk_insert_mappings(mapper=Department, mappings=objects)
        self.session_commit()

    @handle_error
    def insert_jobs(self, objects: List[Dict[str, Any]]) -> None:
        self._session.bulk_insert_mappings(mapper=Job, mappings=objects)
        self.session_commit()

    def insert_to(self, table: str, objects: List[Dict[str, Any]]) -> None:

        if table == EMPLOYEES_TABLE:
            self.insert_employees(objects)
        elif table == DEPARTMENT_TABLE:
            self.insert_departments(objects)
        elif table == JOB_TABLE:
            self.insert_jobs(objects)

    def session_commit(self) -> None:
        self._session.commit()
