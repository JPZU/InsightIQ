from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from apps.dashboard.service import DashboardService

router = APIRouter()


class DashboardSchemaRequest(BaseModel):
    pass


@router.get("/")
def get_schema():
    """Retrieve the dashboard schema."""
    try:
        return DashboardService.get_schema()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting the schema: {str(e)}"
        )


@router.get("/analysis")
def get_analysis():
    """Retrieve analysis data for the dashboard."""
    try:
        return DashboardService.calculate_some_analysis()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting the analysis: {str(e)}"
        )
