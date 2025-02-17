import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from backend.database.models.base import engine  # Import engine from base.py

# Database URL (replace with your actual database URL)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")  # SQLite example
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"  # PostgreSQL example
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"  # MySQL example

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only for SQLite
)

# Create a configured SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)