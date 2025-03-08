from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class VisualResource(Base):
    __tablename__ = "visual_resources"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(length=50))  # "plot" o "table"
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)

    # Relationships
    response_id = Column(Integer, ForeignKey("responses.id"))
    response = relationship("Response", back_populates="visual_resources")