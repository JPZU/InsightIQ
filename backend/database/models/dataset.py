from sqlalchemy import Column, DateTime, Integer, String, func

from database.models.base import Base


class DataSet(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(length=255))
    createdAt = Column(DateTime, nullable=False, default=func.now(), server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, default=func.now(), server_default=func.now(), onupdate=func.now())
