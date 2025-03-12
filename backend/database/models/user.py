from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), nullable=False)
    email = Column(String(length=255), unique=True, index=True, nullable=False)
    password = Column(String(length=255), nullable=False)
    role = Column(String(length=50), nullable=False)
    createdAt = Column(DateTime, default=func.now(), server_default=func.now())
    updatedAt = Column(DateTime, default=func.now(), server_default=func.now(), onupdate=func.now())

    # Relationships
    datasets = relationship("DataSet", back_populates="user", cascade="all, delete-orphan")
    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")
