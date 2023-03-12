import logging

from database.clients.backup_client import BackUpClient
from database.models import EMPLOYEES_TABLE, DEPARTMENT_TABLE, JOB_TABLE


class BackupWorker:
    """
    A wrapper that builds a backup of the database tables, by using a BackUpClient.
    The backup will be avro files, stored in the file system (BACKUP_DIRECTORY_PATH).
    """
    def __init__(self, client: BackUpClient) -> None:
        self.client = client

    def run(self):
        logging.info(f"Building backup of {EMPLOYEES_TABLE} table...")
        self.client.build_backup_for(EMPLOYEES_TABLE)
        logging.info(f"Building backup of {DEPARTMENT_TABLE} table...")
        self.client.build_backup_for(DEPARTMENT_TABLE)
        logging.info(f"Building backup of {JOB_TABLE} table...")
        self.client.build_backup_for(JOB_TABLE)
