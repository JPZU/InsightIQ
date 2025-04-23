from utils.db_manager import DBManager
from utils.i18n import _
from utils.synthetic_manager import SyntheticDataManager


class SyntheticDataService:

    @staticmethod
    def generate_synthetic_data(details: str, table_name: str, num_records: int = 10):
        manager = SyntheticDataManager()
        db_manager = DBManager()

        limit = 10
        MAX_BATCH_SIZE = 40
        MAX_ATTEMPTS = 5

        schema = db_manager.get_table_schema(table_name)
        sample_data = db_manager.get_sample_data(table_name, limit)

        if not schema:
            return {"error": _("table_not_found").format(table_name=table_name)}

        if details and len(details) > 500:
            return {"error": _("error_details_too_long")}

        remainder = num_records
        all_synthetic_data = []
        attempts = 0

        while remainder > 0 and attempts < MAX_ATTEMPTS:
            batch_size = min(MAX_BATCH_SIZE, remainder)
            batch_data = manager.generate_synthetic_data(details, table_name, schema, batch_size, sample_data)
            synthetic_data = manager.format_data(batch_data)

            actual_data = synthetic_data[1:] if len(synthetic_data) > 1 else []

            if actual_data:
                all_synthetic_data.extend(synthetic_data)

            generated_count = len(actual_data)

            if generated_count < batch_size:
                remainder = num_records - len(all_synthetic_data)
                if remainder > 0:
                    print(_(f"Insufficient rows generated ({generated_count}/{batch_size}). Retrying... ({attempts+1}/{MAX_ATTEMPTS})"))
                    attempts += 1
                    continue

            elif generated_count > batch_size:
                print(_(f"Too many rows generated ({generated_count}/{batch_size}). Trimming excess..."))
                all_synthetic_data = all_synthetic_data[:num_records]

            remainder = num_records - len(all_synthetic_data)
            print(_(f"Batch generated: {generated_count}, Remaining: {remainder}"))

            if remainder <= 0:
                break

        if remainder > 0:
            print(_(f"Max attempts reached. Could not generate full {num_records} records."))

        return {
            "table": table_name,
            "schema": schema,
            "synthetic_data": all_synthetic_data[:num_records]
        }
