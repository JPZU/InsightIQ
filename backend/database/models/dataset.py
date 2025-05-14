from sqlalchemy import Column, DateTime, Integer, String, func

from .base import Base


class DataSet(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String(length=255), nullable=False)
    file_path = Column(String(length=255))
    createdAt = Column(DateTime, nullable=False, default=func.now(), server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, default=func.now(), server_default=func.now(), onupdate=func.now())
