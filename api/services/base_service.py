from typing import Dict, Any, List

from flask_api.status import HTTP_201_CREATED

from api.rules import DataRule
from api.utils import service_handle_error
from database import DatabaseClient


class BaseService:

    def __init__(self, db_client: DatabaseClient, rules: List[DataRule]) -> None:
        self.db_client = db_client
        self.rules = rules

    @service_handle_error
    def insert_to_db(self, table: str, objects: List[Dict[str, Any]]) -> Dict[str, Any]:
        # apply filter by rules
        objects = list(filter(lambda o: True in [rule.satisfies(o) for rule in self.rules], objects))
        self.db_client.insert_to(table=table, objects=objects)
        return {
            "message": f"Data inserted in {table} table.",
            "code": HTTP_201_CREATED,
            "status": "Created"
        }

