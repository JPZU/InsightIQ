from typing import List

from fastapi import (APIRouter, Depends, File, Form, HTTPException, Path,
                     UploadFile)

from services.file_manager_service import FileManagerService
from utils.file_manager import FileManager

router = APIRouter()


def get_file_manager_service():
    return FileManagerService()


@router.post("/upload/csv/")
async def upload_csv(
    file: UploadFile = File(...),
    table_name: str = Form("default_table"),
    file_manager_service: FileManagerService = Depends(get_file_manager_service),
):
    file_location = FileManager.save_upload_file(file, table_name)
    response = file_manager_service.upload_csv(file, file_location, table_name)

    return response


@router.post("/upload/excel/")
async def upload_excel(
    table_name: str = Form(...),
    file: UploadFile = File(...),
    file_manager_service: FileManagerService = Depends(get_file_manager_service),
):
    file_location = FileManager.save_upload_file(file, table_name)
    response = file_manager_service.upload_excel(file, file_location, table_name)

    return response


@router.post("/upload/google-sheet")
async def upload_google_sheet(
    table_name: str = Form(...),
    url: str = Form(...),
    file_manager_service: FileManagerService = Depends(get_file_manager_service)
):
    response = file_manager_service.upload_google_sheet(table_name, url)

    return response


@router.get("/tables/", response_model=List[str])
async def get_tables(
    file_manager_service: FileManagerService = Depends(get_file_manager_service),
):
    return file_manager_service.get_tables()


@router.get("/tables/{table_name}/data")
async def get_all_table_data(
    table_name: str = Path(..., description="Name of the table to get data for"),
    file_manager_service: FileManagerService = Depends(get_file_manager_service),
):
    data = file_manager_service.get_all_data(table_name)
    if not data:
        raise HTTPException(status_code=404, detail=f"Table {table_name} not found or empty")

    return {
        "table_name": table_name,
        "data": data
    }


@router.delete("/tables/{table_name}")
async def delete_table(
    table_name: str = Path(..., description="Name of the table to delete"),
    file_manager_service: FileManagerService = Depends(get_file_manager_service),
):
    try:
        success = file_manager_service.delete_table(table_name)
        if not success:
            tables = file_manager_service.get_tables()
            if table_name not in tables:
                raise HTTPException(
                    status_code=404,
                    detail=f"Table {table_name} not found. Available tables: {tables}"
                )
            raise HTTPException(
                status_code=400,
                detail=f"Could not delete table {table_name} (unknown error)"
            )

        return {"message": f"Table {table_name} deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting table: {str(e)}"
        )


@router.put("/tables/{table_name}")
async def update_table(
    table_name: str = Path(..., description="Name of the table to update"),
    file: UploadFile = File(...),
    replace: bool = Form(False),
    file_manager_service: FileManagerService = Depends(get_file_manager_service),
):
    file_location = FileManager.save_upload_file(file, table_name)

    if file.filename.endswith(".csv"):
        response = file_manager_service.update_table_from_csv(table_name, file_location, replace)
    elif file.filename.endswith((".xlsx", ".xls")):
        response = file_manager_service.update_table_from_excel(table_name, file_location, replace)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    return {"message": "Successfully updated table"}


@router.get("/tables/{table_name}/info")
async def get_table_info(
    table_name: str = Path(..., description="Name of the table to get info for"),
    file_manager_service: FileManagerService = Depends(get_file_manager_service),
):
    table_info = file_manager_service.get_table_info(table_name)
    if not table_info:
        raise HTTPException(status_code=404, detail=f"Table {table_name} not found")

    return table_info


@router.post("/update/google-sheets")
async def update_google_sheets(
    file_manager_service: FileManagerService = Depends(get_file_manager_service),
):
    try:
        file_manager_service.fetch_and_update_google_sheets()
        return {"message": "Google Sheets updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating Google Sheets: {str(e)}")
