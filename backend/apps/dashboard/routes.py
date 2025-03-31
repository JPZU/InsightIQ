from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from flask_babel import gettext as _

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
        status_code=500, detail=_("error_schema") + f" {str(e)}"
)



@router.get("/analysis")
def get_analysis():
    """Retrieve analysis data for the dashboard."""
    try:
        return DashboardService.calculate_some_analysis()
    except Exception as e:
        raise HTTPException(
    status_code=500, detail=_("error_analysis") + f" {str(e)}"
    )

