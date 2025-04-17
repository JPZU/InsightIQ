from utils.file_manager import FileManager
from utils.alarm_manager import AlarmManager

class FileManagerService:
    def __init__(self):
        pass

    def upload_csv(self, file, csv_file_path, table_name):
        alarm_manager = AlarmManager()
        FileManager.csv_to_db(csv_file_path, table_name)
        triggered = alarm_manager.evaluate_alarms_for_table(table_name)
        return {
            "info": f"file '{file.filename}' saved and uploaded to table '{table_name}'",
            "triggered_alarms": triggered
        }

    def upload_excel(self, file, excel_file_path, table_name, sheet_name=0):
        alarm_manager = AlarmManager()
        FileManager.excel_to_db(excel_file_path, table_name, sheet_name)
        triggered = alarm_manager.evaluate_alarm(table_name)
        return {
            "info": f"file '{file.filename}' saved and uploaded to table '{table_name}'",
            "triggered_alarms": triggered
        }
