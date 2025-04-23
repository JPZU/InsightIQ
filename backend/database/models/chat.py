from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from .base import Base
from .user import User
from .question import Question
from .response import Response


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), nullable=True)
    createdAt = Column(DateTime, nullable=False, default=func.now(), server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, default=func.now(), server_default=func.now(), onupdate=func.now())

    questions = relationship("Question", back_populates="chat", cascade="all, delete-orphan")
    responses = relationship("Response", back_populates="chat", cascade="all, delete-orphan")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user = relationship("User", back_populates="chats")
