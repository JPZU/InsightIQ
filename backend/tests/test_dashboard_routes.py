from fastapi.testclient import TestClient
from unittest.mock import patch
from fastapi import FastAPI
from apps.dashboard.routes import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


@patch("apps.dashboard.service.DashboardService.get_schema")
def test_get_schema(mock_get_schema):
    mock_get_schema.return_value = {
        "file_name": "test.csv",
        "columns": [
            {"name": "Age", "type": "int64"},
            {"name": "Name", "type": "str"},
            {"name": "Fare", "type": "float64"}
        ]
    }

    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "file_name" in data
    assert "columns" in data
    assert len(data["columns"]) == 3


@patch("apps.dashboard.service.DashboardService.calculate_some_analysis")
def test_get_analysis(mock_calculate_some_analysis):
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

    response = client.get("/analysis")

    assert response.status_code == 200
    data = response.json()
    assert "file_name" in data
    assert "descriptive_statistics" in data
    assert "Age" in data["descriptive_statistics"]
    assert data["descriptive_statistics"]["Age"]["max"] == 80
