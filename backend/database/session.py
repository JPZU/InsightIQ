from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.env_manager import EnvManager
from .models.base import Base

SQLALCHEMY_DATABASE_URL = EnvManager.get_database_url()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = Base
