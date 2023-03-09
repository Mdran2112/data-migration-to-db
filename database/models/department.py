from sqlalchemy import Column, Integer, String, DateTime

from database import Base

TABLE = "departments"
COLS = ["id", "department"]


class Department(Base):
    __tablename__ = TABLE

    id = Column(Integer(), primary_key=True)
    department = Column(String(150), nullable=False)
