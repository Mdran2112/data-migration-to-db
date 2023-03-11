import logging
import sys

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from api.rules import AllFieldsRequired
from api.services.transaction_service import TransactionService
from database import engine, DatabaseClient, Base

Base.metadata.create_all(engine, checkfirst=True)

session = sessionmaker(engine)()
DB_CLIENT = DatabaseClient(session)
SERVICE = TransactionService(db_client=DB_CLIENT, rules=[AllFieldsRequired()])
