from sqlalchemy import Column, DateTime, Integer, String

from .base import Base


class DataSet(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(length=255))
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)
