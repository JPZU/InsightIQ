from utils.db_manager import DBManager
from utils.synthetic_manager import SyntheticDataManager


class SyntheticDataService:

    @staticmethod
    def generate_synthetic_data(details: str, table_name: str, num_records: int = 10):
        manager = SyntheticDataManager()

        limit = 10

        db_manager = DBManager()
        sample_data = db_manager.get_sample_data(table_name, limit)
        schema = db_manager.get_table_schema(table_name)
        details_size = 0

        if details:
            details_size = len(details)

        if details_size > 500:
            return {"error": "Details too long. Please provide a shorter description."}

        if not schema:
            return {"error": f"Table '{table_name}' not found."}

        MAX_BATCH_SIZE = 40
        remainder = num_records

        all_synthetic_data = []

        while (remainder > 0):

            batch_size = min(MAX_BATCH_SIZE, remainder)
            batch_data = manager.generate_synthetic_data(details, table_name, schema, batch_size, sample_data)
            synthetic_data = manager.format_data(batch_data)

            if synthetic_data:
                all_synthetic_data.extend(synthetic_data)

            remainder -= batch_size

            print(f"Generating batch of {batch_size}, Remaining: {remainder}")
            print(f"Generated: {len(synthetic_data)}")

        return {
            "table": table_name,
            "schema": schema,
            "synthetic_data": all_synthetic_data
        }
