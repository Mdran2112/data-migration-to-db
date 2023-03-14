from os.path import join
from typing import Dict, Any

from flask_api.status import HTTP_200_OK

from api.utils import service_handle_error
from database import BusinessMetricsClient


class MetricsService:
    """
    Service for delivering metrics requested by stakeholders.
    It requires a BusinessMetricsClient.
    """

    def __init__(self, db_client: BusinessMetricsClient) -> None:
        self.db_client = db_client

    @service_handle_error
    def get_hired_by_quarters(self, year: int = 2021) -> Dict[str, Any]:
        """

        :param year: DYear of interest.
        :return:
        """
        objs = self.db_client.hired_by_quarter(year)

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

        return {
            "response": objs,
            "code": HTTP_200_OK,
            "status": "Ok"
        }
