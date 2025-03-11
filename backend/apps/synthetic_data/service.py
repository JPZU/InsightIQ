from utils.db_manager import DBManager
from utils.synthetic_manager import SyntheticDataManager


class SyntheticDataService:

    @staticmethod
    def generate_synthetic_data(
            details: str,
            table_name: str,
            num_records: int = 10):
        manager = SyntheticDataManager()

        limit = 4

        db_manager = DBManager()
        sample_data = db_manager.get_sample_data(table_name, limit)
        schema = db_manager.get_table_schema(table_name)

        if not schema:
            return {"error": f"Table '{table_name}' not found."}

        synthetic_data = manager.generate_synthetic_data(
            details, table_name, schema, num_records, sample_data
        )

        return {
            "table": table_name,
            "sample_data": sample_data if sample_data else "No real data available",
            "synthetic_data": synthetic_data,
        }
