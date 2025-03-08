from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255))
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)

    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="chats")
    questions = relationship("Question", back_populates="chat")
    responses = relationship("Response", back_populates="chat")