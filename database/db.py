import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

try:
    engine = create_engine(os.getenv("DATABASE_URL", None))
except:
    raise Exception("Unable to create engine instance. Check if DATABASE_URL environ is defined or is correct.")
Base = declarative_base()