from utils.db_manager import DBManager


class DashboardService:

    @staticmethod
    def get_schema():
        db_manager = DBManager()
        return {"tables": db_manager.infer_csv_schema()}
