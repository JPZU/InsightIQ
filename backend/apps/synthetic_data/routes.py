from fastapi import APIRouter, Query

from apps.synthetic_data.service import SyntheticDataService
from utils.db_manager import DBManager
from utils.i18n import _ 


router = APIRouter()


@router.post("/generate/")
async def generate_data(
    table_name: str = Query(
        ..., description=_("table_name_description")
    ),
    num_records: int = Query(
        10, description=_("num_records_description")
    ),
    details: str = Query(
        None, description=_("details_description")
    ),
):
    return SyntheticDataService.generate_synthetic_data(
        details,
        table_name,
        num_records,
    )


@router.get("/tables/")
async def get_table_names():
    db_manager = DBManager()
    tables = db_manager.get_table_names()
    return {"tables": tables}
