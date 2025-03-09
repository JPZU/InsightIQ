from fastapi.testclient import TestClient
from unittest.mock import patch
from fastapi import FastAPI
from apps.dashboard.routes import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

# ✅ Prueba para el endpoint GET /


@patch("apps.dashboard.service.DashboardService.get_schema")
def test_get_schema(mock_get_schema):
    """
    Prueba el endpoint GET /
    Simula la respuesta de DashboardService.get_schema()
    """
    # Simular la respuesta esperada
    mock_get_schema.return_value = {
        "file_name": "test.csv",
        "columns": [
            {"name": "Age", "type": "int64"},
            {"name": "Name", "type": "str"},
            {"name": "Fare", "type": "float64"}
        ]
    }

    # Hacer la solicitud HTTP simulada
    response = client.get("/")

    # Verificaciones
    assert response.status_code == 200  # Código HTTP correcto
    data = response.json()
    assert "file_name" in data
    assert "columns" in data
    assert len(data["columns"]) == 3  # Esperamos 3 columnas en este test

# Prueba para el endpoint GET /analysis


@patch("apps.dashboard.service.DashboardService.calculate_some_analysis")
def test_get_analysis(mock_calculate_some_analysis):
    """
    Prueba el endpoint GET /analysis
    Simula la respuesta de DashboardService.calculate_some_analysis()
    """
    # Simular la respuesta esperada
    mock_calculate_some_analysis.return_value = {
        "file_name": "test.csv",
        "descriptive_statistics": {
            "Age": {
                "count": 714,
                "mean": 29.7,
                "std": 14.5,
                "min": 0.42,
                "max": 80
            }
        }
    }

    # Hacer la solicitud HTTP simulada
    response = client.get("/analysis")

    # ✅ Verificaciones
    assert response.status_code == 200  # Código HTTP correcto
    data = response.json()
    assert "file_name" in data
    assert "descriptive_statistics" in data
    assert "Age" in data["descriptive_statistics"]
    # Verificar valor esperado
    assert data["descriptive_statistics"]["Age"]["max"] == 80
