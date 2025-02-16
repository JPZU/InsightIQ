from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Define the database URL (SQLite in this case)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Base class for models
Base = declarative_base()