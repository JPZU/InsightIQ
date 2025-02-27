from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Base class for models
Base = declarative_base()

# Example model: User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=255), unique=True, index=True)
    hashed_password = Column(String(length=255))