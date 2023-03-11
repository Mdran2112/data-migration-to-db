from typing import Dict, Any, List

from flask_api.status import HTTP_201_CREATED

from api.rules import DataRule
from api.utils import service_handle_error
from database import DatabaseClient


class TransactionService:
    """
    Service for requesting inserts to the Data Base.
    It requires a DatabaseClient and a list of DataRule.
    """
    def __init__(self, db_client: DatabaseClient, rules: List[DataRule]) -> None:
        self.db_client = db_client
        self.rules = rules

    @service_handle_error
    def insert_to_db(self, table: str, objects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Uses the db_client to insert a series of data objects.
        DataRules will be applied to each object, and those that don't satisfy a rule will be omitted.

        :param table: Database table name.
        :param objects: List of objects to be inserted in the table.
        :return:
        """
        # apply filter by rules
        objects = list(filter(lambda o: True in [rule.satisfies(o) for rule in self.rules], objects))
        self.db_client.insert_to(table=table, objects=objects)
        return {
            "message": f"Data inserted in {table} table.",
            "code": HTTP_201_CREATED,
            "status": "Created"
        }

