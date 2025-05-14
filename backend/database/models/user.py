from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import relationship

from database.models.base import Base
from database.models.alert import Alert


class RoleEnum(PyEnum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(length=255), nullable=False)
    username = Column(String(length=255), nullable=False)
    email = Column(String(length=255), unique=True, index=True, nullable=False)
    password = Column(String(length=255), nullable=False)

    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.USER)

    createdAt = Column(DateTime, default=func.now(), server_default=func.now())
    updatedAt = Column(DateTime, default=func.now(), server_default=func.now(), onupdate=func.now())

    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")
    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")
