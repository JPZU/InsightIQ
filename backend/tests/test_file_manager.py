import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import text

client = TestClient(app)

# --- TESTS BASED ON ACCEPTANCE CRITERIA ---

# Criterion 1: The API should provide a default table when no files have been uploaded
def test_default_table_exists(test_session):
    """Tests that the database contains a default test table."""
    result = test_session.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
    table_names = [row[0] for row in result]
    assert "titanic" in table_names, "The default test table was not found."

# Criterion 2: A CSV file should be uploadable, creating a table in the database
def test_upload_csv(client, sample_csv_file):
    """Tests that a CSV file can be uploaded and a table is created in the database."""
    with open(sample_csv_file, "rb") as file:
        response = client.post(
            "api/file_manager/upload/csv/",
            files={"file": file},
            data={"table_name": "test_table"}
        )

    assert response.status_code == 200
    assert "file 'test_file.csv' saved" in response.json()["info"]

# Criterion 2: An Excel file should be uploadable, creating a table in the database
def test_upload_excel(client, sample_excel_file):
    """Tests that an Excel file can be uploaded and a table is created in the database."""
    with open(sample_excel_file, "rb") as file:
        response = client.post(
            "api/file_manager/upload/excel/",
            files={"file": file},
            data={"table_name": "test_table", "sheet_name": "0"}
        )

    assert response.status_code == 200
    assert "file 'test_file.xlsx' saved" in response.json()["info"]

# Criterion 3: If a new file is uploaded, the previous table should be deleted, leaving only the new one
def test_replace_existing_table(client, sample_csv_file, test_session):
    """Tests that when a new file is uploaded, the previous table is deleted and only the new one remains."""
    with open(sample_csv_file, "rb") as file:
        client.post(
            "/file_manager/upload/csv/",
            files={"file": file},
            data={"table_name": "test_table"}
        )

    # Upload another file to verify that it replaces the previous one
    with open(sample_csv_file, "rb") as file:
        client.post(
            "/file_manager/upload/csv/",
            files={"file": file},
            data={"table_name": "new_table"}
        )

    # Verify that only the new table exists
    result = test_session.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
    table_names = [row[0] for row in result]
    assert "test_table" not in table_names, "The previous table was not deleted."
