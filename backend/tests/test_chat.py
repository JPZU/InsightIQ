from fastapi.testclient import TestClient
from unittest.mock import patch
from fastapi import FastAPI
from apps.chat.routes import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_question_success():
    with patch("apps.chat.service.ChatService.get_response", return_value="Hi, How are you?") as mock_service:
        response = client.post("/", json={"question": "How are you?"})
        assert response.status_code == 200
        assert response.json() == {"response": "Hi, How are you?"}
        mock_service.assert_called_once_with("How are you?")

def test_question_failure():
    with patch("apps.chat.service.ChatService.get_response", return_value=None) as mock_service:
        response = client.post("/", json={"question": "Invalid question"})
        assert response.status_code == 500
        assert response.json() == {"detail": "Failed to process SQL query"}
        mock_service.assert_called_once_with("Invalid question")
