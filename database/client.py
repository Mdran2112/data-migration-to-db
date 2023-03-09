from datetime import date
from typing import List, Dict, Any, Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session

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

    def insert_employees(self, objects: List[Dict[str, Any]]) -> None:
        self._session.bulk_insert_mappings(mapper=Employee, mappings=objects)
        self.session_commit()

    def insert_departments(self, objects: List[Dict[str, Any]]) -> None:
        self._session.bulk_insert_mappings(mapper=Department, mappings=objects)
        self.session_commit()

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
