import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

# 1. Test create alarm using natural language
def test_create_alarm(client, mocker):
    """Tests creating an alarm using natural language."""
    mock_response = {
        "message": "Alarm created successfully.",
        "table_name": "titanic",
        "alarm_details": {
            "field": "age",
            "condition": "less than",
            "threshold": 18,
            "description": "Alert for minors",
        }
    }

    mock_create_alarm = mocker.patch(
        "apps.alarm_management.service.create_alarm_from_natural_language",
        return_value=mock_response
    )

    response = client.post("/alarm_management/create", params={"user_input": "Alert when age is less than 18"})

    assert response.status_code == 200
    assert response.json()["message"] == "Alarm created successfully."
    mock_create_alarm.assert_called_once()

# 2. Test list alarms
def test_list_alarms(client, mocker):
    """Tests retrieving all alarms."""
    mock_alarms = [
        {
            "id": 1,
            "field": "age",
            "condition": "less than",
            "threshold": 18,
            "description": "Alert for minors",
            "table_name": "titanic"
        }
    ]
    mock_get_all = mocker.patch(
        "apps.alarm_management.service.get_all_alarms",
        return_value=mock_alarms
    )

    response = client.get("/alarm_management/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["field"] == "age"
    mock_get_all.assert_called_once()

# 3. Test update alarm partially
def test_create_and_update_alarm():
    create_response = client.post(
        "/alarm_management/create",
        params={"user_input": "Alert when age is greater than 18"}
    )
    assert create_response.status_code == 200
    alarm_data = create_response.json()["alarm_details"]

    alarm_id = alarm_data["id"]

    updated_fields = {
        "threshold": 21,
        "description": "Updated threshold for age"
    }

    update_response = client.patch(f"/alarm_management/update/{alarm_id}", json=updated_fields)
    assert update_response.status_code == 200

    update_data = update_response.json()
    assert update_data["message"] == f"Alarm {alarm_id} updated successfully"

    # Paso 3: Consultar y verificar los cambios
    list_response = client.get("/alarm_management/list")
    assert list_response.status_code == 200

    updated_alarm = next((a for a in list_response.json() if a["id"] == alarm_id), None)
    assert updated_alarm is not None
    assert updated_alarm["threshold"] == 21
    assert updated_alarm["description"] == "Updated threshold for age"

# 4. Test delete alarm by ID
def test_create_and_delete_alarm(client):
    """Creates an alarm and then deletes it, verifying both actions."""
    create_response = client.post(
        "/alarm/create",
        params={"user_input": "Alert when age is greater than 65"}
    )
    assert create_response.status_code == 200
    data = create_response.json()
    assert "alarm_details" in data

    list_response = client.get("/alarm_management/list")
    assert list_response.status_code == 200
    alarms = list_response.json()
    created_alarm = next((a for a in alarms if a["description"] == "Alert when age is greater than 65"), None)
    assert created_alarm is not None

    alarm_id = created_alarm["id"]

    delete_response = client.delete(f"/alarm_management/delete/{alarm_id}")
    assert delete_response.status_code == 200
    assert f"Alarm with ID {alarm_id} deleted successfully" in delete_response.json()["message"]

    list_after_delete = client.get("/alarm_management/list")
    remaining_alarms = list_after_delete.json()
    assert all(a["id"] != alarm_id for a in remaining_alarms)
