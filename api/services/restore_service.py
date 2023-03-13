from os.path import join
from typing import Dict, Any

from flask_api.status import HTTP_200_OK

from api.utils import service_handle_error
from database import DatabaseTransactionClient

from avro.io import DatumReader
from avro.datafile import DataFileReader

from globals import BACKUP_DIRECTORY_PATH


class RestoreService:
    """
    Service for restoring the databases tables from avro files located in the file system.
    It requires a DatabaseClient.
    """

    def __init__(self, db_client: DatabaseTransactionClient) -> None:
        self.db_client = db_client

    @service_handle_error
    def restore(self, table: str) -> Dict[str, Any]:
        """
        Uses the db_client to restore a certain table with its backup.
        It is assumed that the backup is an avro file located in BACKUP_DIRECTORY_PATH. the avro file has to be named
        like the table's name (employees.avro, departments.avro, jobs.avro)

        :param table: Database table name.
        :return:
        """
        reader = DataFileReader(open(join(BACKUP_DIRECTORY_PATH, table + ".avro"), "rb"), DatumReader())
        batch = []
        count = 0
        # all current data in the table will be deleted and replaced with backup data.
        self.db_client.delete(table=table)
        for _object in reader:
            _object: Dict[str, Any]
            batch.append(_object)
            count += 1
            if count == 1000:
                self.db_client.insert_to(table=table, objects=batch)
                batch.clear()

        return {
            "message": "Table restored from avro backup file.",
            "code": HTTP_200_OK,
            "status": "Created"
        }
