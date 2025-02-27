from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.base import Base
from backend.core.config import settings

# Crear la URL de la base de datos
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Crear el motor de SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Verifica la conexión antes de usarla
    pool_recycle=3600,  # Recicla las conexiones después de 1 hora
)

# Crear una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = Base