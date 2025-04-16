from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from apps.detail_report.service import DetailReportService

router = APIRouter()


@router.get("/detail-report", tags=["Reports"])
def get_detailed_report():
    """
    Genera un reporte detallado en texto usando IA.
    """
    try:
        return DetailReportService.generate_consumption_and_turnover_report()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")
