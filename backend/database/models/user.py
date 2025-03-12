from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255))
    email = Column(String(length=255), unique=True, index=True)
    password = Column(String(length=255))
    role = Column(String(length=50))
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)

    # Relationships
    dataSet = relationship("DataSet", back_populates="user", uselist=False)
    chats = relationship("Chat", back_populates="user")
    alerts = relationship("Alert", back_populates="user")
