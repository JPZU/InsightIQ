from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.detail_report.routes import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)
