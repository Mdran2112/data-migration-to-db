from sqlalchemy.orm import sessionmaker

from database import engine, DatabaseClient, Base

Base.metadata.create_all(engine, checkfirst=True)

session = sessionmaker(engine)()
DB_CLIENT = DatabaseClient(session)
