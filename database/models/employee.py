from sqlalchemy import Column, Integer, String, DateTime

from database import Base

TABLE = "employees"
COLS = ["id", "name", "datetime", "department_id", "job_id"]


class Employee(Base):
    __tablename__ = TABLE

    id = Column(Integer(), primary_key=True)
    name = Column(String(150), nullable=False)
    datetime = Column(DateTime(), nullable=False)
    department_id = Column(Integer(), nullable=False)
    job_id = Column(Integer(), nullable=False)
