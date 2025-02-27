from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from backend.core.config import settings  # Importar configuración desde el archivo de configuración

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
Base = declarative_base()