import logging
from typing import List, Dict, Any

from sqlalchemy.engine import Result, Row
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


class BusinessMetricsClient:
    """
    client used for getting metrics of interest related with business data.
    Attributes
    ----------
    session: Session
       SQLAlchemy session.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def _get(self, query: str) -> List[Row]:
        try:
            logging.info(f"The following query will be executed:")
            logging.info(query)
            _objects = self._session.execute(query).fetchall()
            return _objects
        except IntegrityError as ie:
            self._session.rollback()
            raise ie
        except Exception as ex:
            self._session.rollback()
            raise ex

    def hired_by_quarter(self, year: int = 2021) -> List[Row]:
        """
        Gets the number of employees hired for each job and department in a certain year divided by quarter.
        The results are ordered alphabetically by department and job.
        :param year: Year of interest
        :return: List of registries.
                 Example [{"department": Staff, "job": "Recruiter", "Q1": 3, "Q2": 0, "Q3": 7, "Q4": 11}, ...]
        """
        query = f"""
                SELECT d.department, j.job,
                    COUNT(CASE WHEN YEAR(e.datetime) = {year} AND QUARTER(e.datetime) = 1 THEN e.id END) AS Q1,
                    COUNT(CASE WHEN YEAR(e.datetime) = {year} AND QUARTER(e.datetime) = 2 THEN e.id END) AS Q2,
                    COUNT(CASE WHEN YEAR(e.datetime) = {year} AND QUARTER(e.datetime) = 3 THEN e.id END) AS Q3,
                    COUNT(CASE WHEN YEAR(e.datetime) = {year} AND QUARTER(e.datetime) = 4 THEN e.id END) AS Q4
                FROM employees e
                INNER JOIN jobs j ON e.job_id = j.id
                INNER JOIN departments d ON e.department_id = d.id
                WHERE YEAR(e.datetime) = {year}
                GROUP BY d.department, j.job
                ORDER BY d.department ASC, j.job ASC;
        """
        logging.info("Requesting hired employees by quarter...")
        _objects = self._get(query)
        return _objects

    def hired_of_departments(self, year: int = 2021) -> List[Row]:
        """
        Gets the list of department_id, department and number of employees hired of each department that
        hired more employees than the mean of employees hired in 2021 for all departments.
        The results will be ordered by the number of employees hired in descending order.
        :param year: Year of interest
        :return: List of registries.
                 Example [{"id": 4, "department": "Staff", "hired": 45}, ...]
        """
        query = f"""
            SELECT d.id, d.department, COUNT(e.id) AS hired
                FROM employees e
                INNER JOIN departments d ON e.department_id = d.id
                WHERE YEAR(e.datetime) = {year}
                GROUP BY d.id, d.department
                HAVING COUNT(e.id) > (
                    SELECT AVG(hired)
                    FROM (
                        SELECT COUNT(id) AS hired
                        FROM employees
                        WHERE YEAR(datetime) = {year}
                        GROUP BY department_id
                    ) AS employees_per_department
                )
                ORDER BY hired DESC;
            """
        logging.info("Requesting number of employees hired of each department...")
        _objects = self._get(query)
        return _objects
