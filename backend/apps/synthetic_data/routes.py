from fastapi import APIRouter, Query

from apps.synthetic_data.service import SyntheticDataService
from utils.db_manager import DBManager

router = APIRouter()


@router.post("/generate/")
async def generate_data(
        table_name: str = Query(
            ...,
            description="The name of the table to generate synthetic data for"),
    num_records: int = Query(
            10,
            description="Number of synthetic records to generate"),
        details: str = Query(
            None,
            description="Details of the synthetic data you wish to generate"),
):

    return SyntheticDataService.generate_synthetic_data(
        details, table_name, num_records
    )


@router.get("/tables/")
async def get_table_names():
    db_manager = DBManager()
    tables = db_manager.get_table_names()
    return {"tables": tables}
