from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(length=255))
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)

    chat = relationship("Chat", back_populates="questions")
    chat_id = Column(Integer, ForeignKey("chats.id"))
    response = relationship("Response", back_populates="question", uselist=False)
