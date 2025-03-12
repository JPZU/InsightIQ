from utils.file_manager import FileManager


class FileManagerService:
    def __init__(self):
        pass

    def upload_csv(self, csv_file_path, table_name):
        FileManager.csv_to_db(csv_file_path, table_name)

    def upload_excel(self, excel_file_path, table_name, sheet_name=0):
        FileManager.excel_to_db(excel_file_path, table_name, sheet_name)
