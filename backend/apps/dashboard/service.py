from utils.db_manager import DBManager


class DashboardService:

    @staticmethod
    def get_schema():
        db_manager = DBManager()
        df = db_manager.get_dataframe()

        schema = []
        for column_name, dtype in df.dtypes.items():
            schema.append({
                "name": column_name,
                "type": str(dtype)
            })

        return {
            "file_name": "titanic.csv",
            "columns": schema
        }

    @staticmethod
    def calculate_some_analysis():
        db_manager = DBManager()
        df = db_manager.get_dataframe()

        numeric_df = df.select_dtypes(include=['number'])

        descriptive_stats = numeric_df.describe().to_dict()

        for column, stats in descriptive_stats.items():
            descriptive_stats[column] = {
                str(key): value for key, value in stats.items()}

        return {
            "file_name": "titanic.csv",
            "descriptive_statistics": descriptive_stats
        }
