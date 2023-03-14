import json
import logging
import time
from typing import Callable, Dict, Any

from flask.views import MethodView
from flask_api.status import HTTP_200_OK
from flask_smorest import Blueprint

from api import METRICS_SERVICE
from api.controllers import stakeholder_auth

blp = Blueprint("Metrics", "metrics", description="Metrics requested by stakeholder.")


class MetricsEmployeesBase(MethodView):

    service_function: Callable[[int], Dict[str, Any]]

    def get(self, year: int):
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
                  description="""Gets the number of employees hired for each job and department in a certain year divided by quarter.
                                 The results are ordered alphabetically by department and job.""",
                  example={
                      "message": ".",
                      "code": HTTP_200_OK,
                      "status": "Ok"
                  })
    def get(self, year: int):
        res, code = super().get(year)
        return res, code


@blp.route("/metrics/<int:year>/employees/departments")
class MetricsEmployeesDepartmentsController(MetricsEmployeesBase):

    service_function: Callable[[int], Dict[str, Any]] = METRICS_SERVICE.get_hired_of_departments

    @stakeholder_auth.login_required
    @blp.response(HTTP_200_OK,
                  description="""Gets the list of department_id, department and number of employees hired of each department that
                                hired more employees than the mean of employees hired in 2021 for all departments.
                                The results will be ordered by the number of employees hired in descending order.""",
                  example={
                      "message": ".",
                      "code": HTTP_200_OK,
                      "status": "Ok"
                  })
    def get(self, year: int):
        res, code = super().get(year)
        return res, code
