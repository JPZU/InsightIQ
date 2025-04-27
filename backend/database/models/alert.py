from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    condition = Column(String(255))          
    description = Column(Text)               
    field = Column(String(255))            
    is_active = Column(Boolean, default=True, nullable=False)
    table_name = Column(String(255))       
    threshold = Column(Integer)              

    createdAt = Column(DateTime, nullable=False, default=func.now(), server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, default=func.now(), server_default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="alerts")
