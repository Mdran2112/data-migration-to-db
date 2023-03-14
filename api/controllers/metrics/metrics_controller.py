import json
import logging
import time
from typing import Callable, Dict, Any

from flask.views import MethodView
from flask_api.status import HTTP_200_OK
from flask_smorest import Blueprint

from api import METRICS_SERVICE
from api.controllers import stakeholder_auth

import json

blp = Blueprint("Metrics", "metrics", description="Metrics requested by stakeholder.")


class MetricsEmployeesBase(MethodView):
    service_function: Callable[[int], Dict[str, Any]]

    def put(self, year: int):
        t0 = time.time()
        logging.info(f"Requesting metrics...")
        logging.info(f"Year: {year}")

        res = self.service_function(year)

        tf = time.time()

        total_time = tf - t0

        logging.info(f"Finished! Time: {round(total_time, 2)} secs.")
        logging.info(f"{json.dumps(res, indent=4)}")

        return res, res.get("code")


@blp.route("/metrics/<int:year>/employees/quarters")
class MetricsEmployeesQuartersController(MetricsEmployeesBase):
    service_function: Callable[[int], Dict[str, Any]] = METRICS_SERVICE.get_hired_by_quarters

    @stakeholder_auth.login_required
    @blp.response(HTTP_200_OK,
                  description="""Creates a visual report of employees hired for each job and department in a certain year divided by quarter.
                                 The results are ordered alphabetically by department and job. 
                                 The report will be saved in the file system.""",
                  example={
                      "response": [
                          {
                              "Q1": 1,
                              "Q2": 0,
                              "Q3": 0,
                              "Q4": 0,
                              "department": "Accounting",
                              "job": "Account Representative IV"
                          },
                          {
                              "Q1": 0,
                              "Q2": 1,
                              "Q3": 0,
                              "Q4": 0,
                              "department": "Accounting",
                              "job": "Actuary"
                          }
                      ],
                      "code": HTTP_200_OK,
                      "status": "Ok"
                  })
    def put(self, year: int):
        res, code = super().put(year)
        return res, code


@blp.route("/metrics/<int:year>/employees/departments")
class MetricsEmployeesDepartmentsController(MetricsEmployeesBase):
    service_function: Callable[[int], Dict[str, Any]] = METRICS_SERVICE.get_hired_of_departments

    @stakeholder_auth.login_required
    @blp.response(HTTP_200_OK,
                  description="""Creates a visual report of department_id, department and number of employees hired of each department that
                                hired more employees than the mean of employees hired in 2021 for all departments.
                                The results will be ordered by the number of employees hired in descending order. 
                                The report will be saved in the file system.""",
                  example={
                      "response": [
                        {
                          "department": "Support",
                          "hired": 216,
                          "id": 8
                        },
                        {
                          "department": "Engineering",
                          "hired": 205,
                          "id": 5
                        }
                      ],
                      "code": HTTP_200_OK,
                      "status": "Ok"
                  })
    def put(self, year: int):
        res, code = super().put(year)
        return res, code
