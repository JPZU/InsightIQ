from sqlalchemy.orm import sessionmaker
from backend.database.models.base import engine  # Import engine from base.py

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)