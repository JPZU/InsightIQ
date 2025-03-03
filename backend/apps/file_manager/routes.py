from fastapi import APIRouter, UploadFile, File, Depends
from .service import FileManagerService
from utils.file_manager import FileManager

router = APIRouter()

def get_file_manager_service():
    return FileManagerService()

@router.post("/upload/csv/")
async def upload_csv(file: UploadFile = File(...), table_name: str = "default_table", file_manager_service: FileManagerService = Depends(get_file_manager_service)):
    # Save the uploaded file to a temporary location
    file_location = FileManager.save_upload_file(file, f"temp/{file.filename}")
    # Upload the CSV file to the database
    file_manager_service.upload_csv(file_location, table_name)
    return {"info": f"file '{file.filename}' saved at '{file_location}' and uploaded to table '{table_name}'"}

@router.post("/upload/excel/")
async def upload_excel(file: UploadFile = File(...), table_name: str = "default_table", sheet_name: int = 0, file_manager_service: FileManagerService = Depends(get_file_manager_service)):
    # Save the uploaded file to a temporary location
    file_location = FileManager.save_upload_file(file, f"temp/{file.filename}")
    # Upload the Excel file to the database
    file_manager_service.upload_excel(file_location, table_name, sheet_name)
    return {"info": f"file '{file.filename}' saved at '{file_location}' and uploaded to table '{table_name}'"}