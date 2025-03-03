from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from apps.dashboard.service import DashboardService

router = APIRouter()


class DashboardSchemaRequest(BaseModel):
    pass  # No tienes parámetros para inferir el schema, pero se puede extender en el futuro


@router.get("/")
def get_schema():
    """
    Endpoint para obtener el esquema inferido del CSV.
    """
    try:
        schema = DashboardService.get_schema()
        return schema
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener el esquema: {str(e)}")
