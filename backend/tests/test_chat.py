import time

from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.chat.routes import router

app = FastAPI()
app.include_router(router, prefix="/api/chat")

client = TestClient(app)


def test_chat_response_includes_output():
    response = client.post(
        "/api/chat/",
        json={
            "question": "What was the total revenue last quarter?"})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

    data = response.json()

    assert "response" in data, "Response does not contain 'response' key."
    assert "output" in data["response"], "Response does not contain 'output' key inside 'response'."
    assert isinstance(data["response"]["output"],
                      str), "'output' field is not a string."
    assert data["response"]["output"].strip(), "'output' field is empty."


def test_chat_includes_generated_query():
    response = client.post(
        "/api/chat/",
        json={
            "question": "How many users signed up last month?"})
    assert response.status_code == 200, f"Expected 200, got {
        response.status_code}. Response: {
        response.text}"

    data = response.json()

    assert "response" in data, "Response does not contain 'response' key."
    assert "query" in data["response"], "Response does not contain 'query' key inside 'response'."
    assert isinstance(data["response"]["query"],
                      str), "'query' field is not a string."
    assert data["response"]["query"].strip(), "'query' field is empty."


def test_chat_includes_query_results():
    response = client.post(
        "/api/chat/",
        json={
            "question": "What is the customer count for 2024?"})
    assert response.status_code == 200, f"Expected 200, got {
        response.status_code}. Response: {
        response.text}"

    data = response.json()

    assert "response" in data, "Response does not contain 'response' key."
    assert "query_output" in data["response"], "Response does not contain 'query_output' key inside 'response'."
    assert isinstance(data["response"]["query_output"], (str, list)
                      ), "'query_output' field is not a string or list."
    assert data["response"]["query_output"], "'query_output' field is empty."


def test_chat_response_time_less_than_30_seconds():
    start_time = time.time()

    response = client.post(
        "/api/chat/",
        json={"question": "Give me a summary of sales for the past year"}
    )

    end_time = time.time()
    elapsed_time = end_time - start_time

    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

    assert elapsed_time < 30, f"Response took {elapsed_time:.2f} seconds, which exceeds the 30 second limit"

    data = response.json()
    assert "response" in data, "Response does not contain 'response' key."
