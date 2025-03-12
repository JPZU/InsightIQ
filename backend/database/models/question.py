from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(length=255))
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)

    # Relationships
    chat_id = Column(Integer, ForeignKey("chats.id"))
    chat = relationship("Chat", back_populates="questions")
    response = relationship(
        "Response",
        back_populates="question",
        uselist=False)
