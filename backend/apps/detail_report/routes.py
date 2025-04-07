from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from apps.detail_report.service import DetailReportService

router = APIRouter()


@router.get("/inventory_summary")
def get_inventory_summary():
    try:
        return DetailReportService.get_inventory_summary()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting data: {str(e)}"
        )


@router.get("/turnover_analysis_by_region")
def get_turnover_analysis_by_region():
    try:
        return DetailReportService.get_turnover_analysis_by_region()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting data: {str(e)}"
        )


@router.get("/restock_recommendations")
def get_restock_recommendations():
    try:
        return DetailReportService.get_restock_recommendations()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting data: {str(e)}"
        )
