from apps.detail_report.routes import router
from fastapi.testclient import TestClient
from unittest.mock import patch
from fastapi import FastAPI

app = FastAPI()
app.include_router(router, prefix="/api/detail_report")
client = TestClient(app)


@patch("apps.detail_report.service.DetailReportService.generate_consumption_and_turnover_report")
def test_get_detailed_report(mock_generate_report):
    mock_generate_report.return_value = {
        "report_text": """## Inventory Status Summary
                - Inventory is stable overall.
                ## High and Low Turnover Products
                - High: Product A, Product B.
                - Low: Product X, Product Y.
                ## Restocking Recommendations
                - Restock Product A and Product B.
                ## Conclusion
                Focus on high-demand products.""",
        "date": "2025-04-16T12:34:56"
    }

    response = client.get("/api/detail_report/detail-report")

    assert response.status_code == 200
    data = response.json()

    assert "report_text" in data
    assert "date" in data

    report_text = data["report_text"]
    assert "Inventory Status Summary" in report_text
    assert "High and Low Turnover Products" in report_text
    assert "Restocking Recommendations" in report_text
    assert "Conclusion" in report_text
