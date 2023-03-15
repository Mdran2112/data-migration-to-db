import logging
from os.path import join
from typing import Dict, Any, List

import pandas as pd
import plotly.express as px


from flask_api.status import HTTP_200_OK

from api.utils import service_handle_error
from database import BusinessMetricsClient
from globals import REPORTS_DIRECTORY_PATH



class MetricsService:
    """
    Service for delivering metrics requested by stakeholders.
    It requires a BusinessMetricsClient.
    """

    def __init__(self, db_client: BusinessMetricsClient) -> None:
        self.db_client = db_client

    @staticmethod
    def _plot_report_and_save(objs: List[Dict[str, Any]], x: str, y: List[str],
                              html_filename: str):
        logging.info("Generating plot box...")
        df = pd.DataFrame({
            x: list(map(lambda o: o[x], objs)),
        })
        for y_n in y:
            df[y_n] = list(map(lambda o: o[y_n], objs))
        fig = px.histogram(df, x=x, y=y, barmode='group')
        output_filepath = join(REPORTS_DIRECTORY_PATH, html_filename)
        fig.write_html(output_filepath)
        logging.info(f"Plot box saved into file system: {output_filepath}...")


    @service_handle_error
    def get_hired_by_quarters(self, year: int = 2021) -> Dict[str, Any]:
        """

        :param year: Year of interest.
        :return:
        """
        objs = self.db_client.hired_by_quarter(year)
        for x in ["department", "job"]:
            self._plot_report_and_save(objs=objs, x=x, y=["Q1", "Q2", "Q3", "Q4"],
                                       html_filename=f"hired_employees_by_{x}_quarters.html")

        return {
            "response": objs,
            "code": HTTP_200_OK,
            "status": "Ok"
        }

    @service_handle_error
    def get_hired_of_departments(self, year: int = 2021) -> Dict[str, Any]:
        """

        :param year: Year of interest.
        :return:
        """
        objs = self.db_client.hired_of_departments(year)
        self._plot_report_and_save(objs=objs, x="department", y=["hired"],
                                   html_filename="hired_employees_of_departments.html")


        return {
            "response": objs,
            "code": HTTP_200_OK,
            "status": "Ok"
        }
