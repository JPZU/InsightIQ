from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from apps.dashboard.service import DashboardService

router = APIRouter()


class DashboardSchemaRequest(BaseModel):
    pass


@router.get("/")
def get_schema():
    try:
        schema = DashboardService.get_schema()
        return schema
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting the schematic: {str(e)}")


@router.get("/analysis")
def get_schema():
    try:
        analysis = DashboardService.calculate_some_analysis()
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting the schematic: {str(e)}")
