from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(length=255))
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)

    # Relationships
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="response")
    chat_id = Column(Integer, ForeignKey("chats.id"))
    chat = relationship("Chat", back_populates="responses")
    visual_resources = relationship("VisualResource", back_populates="response")