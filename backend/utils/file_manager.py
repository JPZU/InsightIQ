import os

import pandas as pd
from fastapi import UploadFile
from sqlalchemy import inspect
from sqlalchemy.sql import text

from utils.db_manager import DBManager


class FileManager:

    @staticmethod
    def load_csv(csv_path):
        """
        Loads a CSV file and returns a pandas DataFrame.
        """
        return pd.read_csv(csv_path)

    @staticmethod
    def load_excel(excel_path, sheet_name=None):
        """
        Loads an Excel file and returns a pandas DataFrame.
        """
        return pd.read_excel(excel_path, sheet_name=sheet_name)

    @staticmethod
    def clear_db_except_titanic(db_manager: DBManager):
        """
        Removes all tables from the database except for 'titanic'.
        This ensures that only one additional dataset exists at any time.
        """
        inspector = inspect(db_manager.engine)
        tables = inspector.get_table_names()

        with db_manager.engine.connect() as conn:
            for table in tables:
                if table != "titanic":
                    conn.execute(text(f"DROP TABLE {table}"))
            conn.commit()

    @staticmethod
    def save_to_csv(df, file_path):
        """
        Saves a pandas DataFrame to a CSV file.
        """
        df.to_csv(file_path, index=False)

    @staticmethod
    def save_to_excel(df, file_path, sheet_name="Sheet1"):
        """
        Saves a pandas DataFrame to an Excel file.
        """
        with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    @staticmethod
    def insert_dataframe_to_table(df: pd.DataFrame, table_name: str, db_manager: DBManager):
        """
        Inserts a pandas DataFrame into a database table.
        """
        df.to_sql(
            table_name,
            db_manager.engine,
            if_exists="replace",
            index=False)

    @staticmethod
    def csv_to_db(csv_file_path, table_name):
        """
        Reads a CSV file and inserts it into a database table.
        Before inserting, it removes any existing tables except 'titanic'.
        """
        db_manager = DBManager()
        FileManager.clear_db_except_titanic(
            db_manager
        )  # Remove tables before inserting
        df = pd.read_csv(csv_file_path)
        FileManager.insert_dataframe_to_table(df, table_name, db_manager)

    @staticmethod
    def excel_to_db(excel_file_path, table_name, sheet_name=0):
        """
        Reads an Excel file and inserts it into a database table.
        Before inserting, it removes any existing tables except 'titanic'.
        """
        db_manager = DBManager()
        FileManager.clear_db_except_titanic(db_manager)

        try:
            sheet_name = int(sheet_name)
        except ValueError:
            pass

        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        FileManager.insert_dataframe_to_table(df, table_name, db_manager)

    @staticmethod
    def save_upload_file(upload_file: UploadFile, table_name: str) -> str:
        """
        Saves an uploaded file to the 'data' directory while ensuring that only 'titanic.csv'
        and the latest uploaded file remain in the directory.
        """
        data_folder = "data"
        os.makedirs(data_folder, exist_ok=True)

        file_extension = upload_file.filename.split(".")[-1]
        destination = os.path.join(data_folder, f"{table_name}.{file_extension}")

        # Get the list of files in 'data' excluding 'titanic.csv'
        existing_files = [
            f for f in os.listdir(data_folder) if f not in [
                "titanic.csv", "db.sqlite"]]

        # If there is an existing file (other than 'titanic.csv'), delete it
        for file in existing_files:
            file_path = os.path.join(data_folder, file)
            os.remove(file_path)

        with open(destination, "wb+") as file_object:
            file_object.write(upload_file.file.read())

        return destination
