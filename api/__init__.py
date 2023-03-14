import logging
import sys

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s;%(levelname)s;%(message)s")

from api.rules import AllFieldsRequired
from api.services.transaction_service import TransactionService
from api.services.restore_service import RestoreService
from api.services.metrics_service import MetricsService
from database import engine, DatabaseTransactionClient, Base, BusinessMetricsClient, BackUpClient

Base.metadata.create_all(engine, checkfirst=True)

session = sessionmaker(engine)()
# Clients
DB_CLIENT = DatabaseTransactionClient(session)
BACKUP_CLIENT = BackUpClient(session)
BUSINESS_METRICS_CLIENT = BusinessMetricsClient(session)

# Services
TRANSACTION_SERVICE = TransactionService(db_client=DB_CLIENT, rules=[AllFieldsRequired()])
RESTORE_SERVICE = RestoreService(db_client=DB_CLIENT)
METRICS_SERVICE = MetricsService(db_client=BUSINESS_METRICS_CLIENT)
