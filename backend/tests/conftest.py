import pandas as pd
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base
from main import app

# URL de la base de datos en memoria para pruebas
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def client():
    """Proporciona un cliente de prueba de FastAPI."""
    return TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    """Configura la base de datos en memoria y carga la tabla 'titanic' antes de cada prueba."""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # Crear las tablas en la base de datos en memoria
    Base.metadata.create_all(bind=engine)

    # Crear la tabla 'titanic' desde el CSV
    try:
        df = pd.read_csv("data/titanic.csv")  # Cargar CSV
        df.to_sql("titanic", con=engine, index=False, if_exists="replace")  # Crear tabla
    except Exception as e:
        print(f"Error cargando 'titanic.csv': {e}")

    yield engine  # Proporcionar la base de datos para las pruebas

    session.close()  # Cerrar sesión
    engine.dispose()  # Liberar recursos


@pytest.fixture(scope="function")
def test_session(test_db):
    """Proporciona una sesión de base de datos para cada prueba."""
    SessionLocal = sessionmaker(bind=test_db)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
def sample_csv_file(tmp_path):
    """Genera un archivo CSV temporal para pruebas."""
    csv_content = "id,name,email\n1,Test User,test@example.com"
    file_path = tmp_path / "test_file.csv"
    file_path.write_text(csv_content)
    return file_path


@pytest.fixture(scope="function")
def sample_excel_file(tmp_path):
    """Genera un archivo Excel temporal para pruebas."""
    data = {"id": [1], "name": ["Test User"], "email": ["test@example.com"]}
    df = pd.DataFrame(data)
    file_path = tmp_path / "test_file.xlsx"
    df.to_excel(file_path, index=False)
    return file_path
