from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class DataSet(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    file = Column(String(length=255))
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)

    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="dataSet")
