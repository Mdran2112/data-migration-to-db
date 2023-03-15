import json
import logging
import time
from io import BytesIO
from os.path import join, basename
from typing import Callable, Dict, Any
from zipfile import ZipFile

from flask import send_file
from flask.views import MethodView
from flask_api.status import HTTP_200_OK
from flask_smorest import Blueprint

from api import METRICS_SERVICE
from api.controllers import stakeholder_auth

import json

from globals import REPORTS_DIRECTORY_PATH

blp = Blueprint("Metrics", "metrics", description="Metrics requested by stakeholder. Creates a visual report and "
                                                  "stores them in the file system (reports volume)")


class MetricsEmployeesBase(MethodView):
    service_function: Callable[[int], Dict[str, Any]]

    def response(self, res: Dict[str, Any]):
        return res, res.get("code")

    def get(self, year: int):
        t0 = time.time()
        logging.info(f"Requesting metrics...")
        logging.info(f"Year: {year}")

        res = self.service_function(year)

        tf = time.time()

        total_time = tf - t0

        logging.info(f"Finished! Time: {round(total_time, 2)} secs.")
        logging.info(f"{json.dumps(res, indent=4)}")

        return self.response(res)


@blp.route("/metrics/<int:year>/employees/quarters")
class MetricsEmployeesQuartersController(MetricsEmployeesBase):
    service_function: Callable[[int], Dict[str, Any]] = METRICS_SERVICE.get_hired_by_quarters

    @stakeholder_auth.login_required
    @blp.response(HTTP_200_OK,
                  description="""Gets a list of employees hired for each job and department in a certain year divided 
                  by quarter. The results are ordered alphabetically by department and job""",
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
    def get(self, year: int):
        res, code = super().get(year)

        return res, code


@blp.route("/metrics/<int:year>/employees/departments")
class MetricsEmployeesDepartmentsController(MetricsEmployeesBase):
    service_function: Callable[[int], Dict[str, Any]] = METRICS_SERVICE.get_hired_of_departments

    @stakeholder_auth.login_required
    @blp.response(HTTP_200_OK,
                  description="""Gets a list of department_id, department and number of employees hired 
                  of each department that hired more employees than the mean of employees hired in 2021 for all 
                  departments. The results will be ordered by the number of employees hired in descending order.""",
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
    def get(self, year: int):
        res, code = super().get(year)

        return res, code


@blp.route("/metrics/<int:year>/employees/quarters/visual-report")
class ReportMetricsEmployeesQuartersController(MetricsEmployeesBase):
    service_function: Callable[[int], Dict[str, Any]] = METRICS_SERVICE.visual_report_hired_by_quarters

    def response(self, res: Dict[str, Any]):
        stream = BytesIO()
        with ZipFile(stream, 'w') as zf:
            for file in [join(REPORTS_DIRECTORY_PATH, "hired_employees_by_department_quarters.html"),
                         join(REPORTS_DIRECTORY_PATH, "hired_employees_by_job_quarters.html")]:
                zf.write(file, basename(file))
        stream.seek(0)

        return send_file(
            stream,
            as_attachment=True,
            download_name='hired_employees_by_quarters.zip'
        )

    @stakeholder_auth.login_required
    @blp.response(HTTP_200_OK,
                  description="""Creates a visual report of employees hired for each job and department in a certain year divided by quarter.
                                 The results are ordered alphabetically by department and job.
                                 The report will be downloaded as a HTML file.""")
    def get(self, year: int):
        resp = super().get(year)

        return resp


@blp.route("/metrics/<int:year>/employees/departments/visual-report")
class ReportMetricsEmployeesDepartmentsController(MetricsEmployeesBase):
    service_function: Callable[[int], Dict[str, Any]] = METRICS_SERVICE.visual_report_hired_of_departments

    def response(self, res: Dict[str, Any]):
        return send_file(path_or_file=join(REPORTS_DIRECTORY_PATH, "hired_employees_of_departments.html"),
                         as_attachment=True)

    @stakeholder_auth.login_required
    @blp.response(HTTP_200_OK,
                  description="""Creates a visual report of department_id, department and number of employees hired 
                  of each department that hired more employees than the mean of employees hired in 2021 for all 
                  departments. The results will be ordered by the number of employees hired in descending order.
                  The report will be downloaded as a HTML file.""")
    def get(self, year: int):
        resp = super().get(year)

        return resp
