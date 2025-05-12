from fastapi import APIRouter, Depends, File, Form, UploadFile

from utils.file_manager import FileManager

from .service import FileManagerService

router = APIRouter()


def get_file_manager_service():
    return FileManagerService()


@router.post("/upload/csv/")
async def upload_csv(
    file: UploadFile = File(...),
    table_name: str = Form("default_table"),
    file_manager_service: FileManagerService = Depends(get_file_manager_service),
):
    # Save the uploaded file to a temporary location
    file_location = FileManager.save_upload_file(file, table_name)
    # Upload the CSV file to the database
    return file_manager_service.upload_csv(file, file_location, table_name)


@router.post("/upload/excel/")
async def upload_excel(
    table_name: str = Form(...),
    sheet_name: int = Form(0),
    file: UploadFile = File(...),
    file_manager_service: FileManagerService = Depends(get_file_manager_service),
):
    # Save the uploaded file to a temporary location
    file_location = FileManager.save_upload_file(file, table_name)
    # Upload the Excel file to the database
    return file_manager_service.upload_excel(file, file_location, table_name, sheet_name)
