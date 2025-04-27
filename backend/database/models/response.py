from sqlalchemy import Column, DateTime, ForeignKey, Integer, func, Text, JSON
from sqlalchemy.orm import relationship

from .base import Base
from .question import Question


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    query_result = Column(JSON)
    createdAt = Column(DateTime, nullable=False, default=func.now(), server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, default=func.now(), server_default=func.now(), onupdate=func.now())

    chat = relationship("Chat", back_populates="responses")
    chat_id = Column(Integer, ForeignKey("chats.id"))

    question = relationship("Question", back_populates="response")
    question_id = Column(Integer, ForeignKey("questions.id"))
