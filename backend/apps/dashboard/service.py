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

        # Filtrar solo columnas numéricas (int, float)
        numeric_df = df.select_dtypes(include=['number'])

        # Calcular estadísticas descriptivas (describe solo numéricas)
        descriptive_stats = numeric_df.describe().to_dict()

        # Opcional: convertir percentiles a strings para asegurar compatibilidad JSON
        for column, stats in descriptive_stats.items():
            descriptive_stats[column] = {
                str(key): value for key, value in stats.items()}

        return {
            "file_name": "titanic.csv",
            "descriptive_statistics": descriptive_stats
        }
