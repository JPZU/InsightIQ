import pandas as pd
from fastapi import UploadFile
from utils.db_manager import DBManager
import os

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
        df.to_sql(table_name, db_manager.engine, if_exists='replace', index=False)

    @staticmethod
    def csv_to_db(csv_file_path, table_name):
        """
        Reads a CSV file and inserts it into a database table.
        """
        db_manager = DBManager()
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        # Insert the DataFrame into the database table
        FileManager.insert_dataframe_to_table(df, table_name, db_manager)

    @staticmethod
    def excel_to_db(excel_file_path, table_name, sheet_name=0):
        """
        Reads an Excel file and inserts it into a database table.
        """
        db_manager = DBManager()
        # Read the Excel file
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        # Insert the DataFrame into the database table
        FileManager.insert_dataframe_to_table(df, table_name, db_manager)

    @staticmethod
    def save_upload_file(upload_file: UploadFile, destination: str) -> str:
        """
        Saves an uploaded file to a temporary location.
        """
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with open(destination, "wb+") as file_object:
            file_object.write(upload_file.file.read())
        return destination