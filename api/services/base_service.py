from typing import Dict, Any, List

from flask_api.status import HTTP_201_CREATED

from api.utils import service_handle_error
from database import DatabaseClient


class BaseService:

    def __init__(self, db_client: DatabaseClient) -> None:
        self.db_client = db_client

    @service_handle_error
    def insert_to_db(self, table: str, objects: List[Dict[str, Any]]) -> Dict[str, Any]:
        self.db_client.insert_to(table=table, objects=objects)
        return {
            "message": f"Data inserted in {table} table.",
            "code": HTTP_201_CREATED,
            "status": "Created"
        }

