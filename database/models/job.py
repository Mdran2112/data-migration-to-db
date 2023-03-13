from sqlalchemy import Column, Integer, String

from database import Base

TABLE = "jobs"
COLS = ["id", "job"]


class Job(Base):
    __tablename__ = TABLE

    id = Column(Integer(), primary_key=True)
    job = Column(String(150), nullable=False)
