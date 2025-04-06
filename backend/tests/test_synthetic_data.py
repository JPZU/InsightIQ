from unittest.mock import patch

import pytest

from apps.synthetic_data.service import SyntheticDataService
from utils.synthetic_manager import SyntheticDataManager


@pytest.fixture(scope="module")
def service():
    return SyntheticDataService()


def test_exact_number_of_rows(service):
    num_records = 49
    response = service.generate_synthetic_data(details="", table_name="titanic", num_records=num_records)
    assert len(response["synthetic_data"]) == num_records


def test_schema_consistency(service):
    response = service.generate_synthetic_data(details="", table_name="titanic", num_records=5)

    db_schema_columns = {col["column_name"] for col in response["schema"]}

    if response["synthetic_data"]:
        llm_schema_columns = set(response["synthetic_data"][0].keys())
    else:
        llm_schema_columns = set()

    assert all(isinstance(row, dict) for row in response["synthetic_data"]), "Synthetic data must be a list of dictionaries"

    assert llm_schema_columns == db_schema_columns, f"Schema mismatch: LLM: {llm_schema_columns}, DB: {db_schema_columns}"


def test_batch_processing_constraint(service):
    num_records = 100
    max_batch_size = 40

    with patch("utils.synthetic_manager.SyntheticDataManager.generate_synthetic_data", wraps=SyntheticDataManager().generate_synthetic_data) as mock_generate:
        response = service.generate_synthetic_data(details="", table_name="titanic", num_records=num_records)

        calls = mock_generate.call_args_list
        batch_sizes_requested = [call.args[3] for call in calls]

        assert all(batch_size <= max_batch_size for batch_size in batch_sizes_requested), f"Exceeded batch limit: {batch_sizes_requested}"

        assert len(response["synthetic_data"]) == num_records
