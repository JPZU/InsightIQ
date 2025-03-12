from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

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
    assert data["file_name"] == "test.csv"

    assert "columns" in data
    assert len(data["columns"]) == 3

    expected_columns = {
        "Age": "int64",
        "Name": "str",
        "Fare": "float64"
    }
    for col in data["columns"]:
        assert col["name"] in expected_columns
        assert col["type"] == expected_columns[col["name"]]


@patch("apps.dashboard.service.DashboardService.calculate_some_analysis")
def test_get_analysis(mock_calculate_some_analysis):
    """
    Verifica que el dashboard muestra correctamente los análisis estadísticos.
    """
    mock_calculate_some_analysis.return_value = {
        "file_name": "test.csv",
        "descriptive_statistics": {
            "Age": {
                "count": 714,
                "mean": 29.7,
                "std": 14.5,
                "min": 0.42,
                "25%": 20.0,
                "50%": 28.0,
                "75%": 38.0,
                "max": 80
            },
            "Fare": {
                "count": 891,
                "mean": 32.2,
                "std": 49.7,
                "min": 0.0,
                "25%": 7.91,
                "50%": 14.45,
                "75%": 31.0,
                "max": 512.3
            }
        }
    }

    response = client.get("/analysis")

    assert response.status_code == 200
    data = response.json()

    assert "file_name" in data
    assert data["file_name"] == "test.csv"

    assert "descriptive_statistics" in data
    assert len(data["descriptive_statistics"]) > 0

    for column, stats in data["descriptive_statistics"].items():
        assert "count" in stats
        assert "std" in stats
        assert "min" in stats
        assert "max" in stats
        assert "25%" in stats
        assert "50%" in stats
        assert "75%" in stats
        assert isinstance(stats["count"], (int, float))
        assert isinstance(stats["std"], (int, float))
