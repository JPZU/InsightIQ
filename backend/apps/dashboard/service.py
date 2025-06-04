import numpy as np

from utils.db_manager import DBManager


class DashboardService:

    @staticmethod
    def get_schema():
        db_manager = DBManager()
        df, file_name = db_manager.get_dataframe()

        schema = []
        for column_name, dtype in df.dtypes.items():
            schema.append({"name": column_name, "type": str(dtype)})

        return {
            "file_name": file_name,
            "columns": schema
        }

    @staticmethod
    def calculate_some_analysis():
        db_manager = DBManager()
        df, file_name = db_manager.get_dataframe()

        # Select only numeric columns
        numeric_df = df.select_dtypes(include=["number"])

        # Exclude columns that look like IDs
        columns_to_analyze = [col for col in numeric_df.columns if 'id' not in col.lower()]
        
        # Keep only desired columns
        cleaned_df = numeric_df[columns_to_analyze]

        # Replace inf and -inf with NaN
        cleaned_df = cleaned_df.replace([float('inf'), float('-inf')], np.nan)

        # Replace NaN with 0
        cleaned_df = cleaned_df.fillna(0)

        # Get descriptive statistics
        descriptive_stats = cleaned_df.describe().to_dict()

        # Ensure all keys are strings and no values are None
        for column, stats in descriptive_stats.items():
            descriptive_stats[column] = {
                str(key): (value if value is not None else 0) for key, value in stats.items()
            }

        return {
            "file_name": file_name,
            "descriptive_statistics": descriptive_stats
        }
