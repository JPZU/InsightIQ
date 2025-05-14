import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
from fastapi import HTTPException, UploadFile
from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from database.models.dataset import DataSet
from database.session import SessionLocal
from utils.db_manager import DBManager


class FileManagerService:
    def __init__(self):
        self.db_manager = DBManager()
        self.session = SessionLocal()

    def __del__(self):
        self.session.close()

    def _store_dataset_info(self, table_name: str, file_path: str) -> None:
        dataset = DataSet(
            table_name=table_name,
            file_path=file_path,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        self.session.add(dataset)
        self.session.commit()

    def upload_csv(self, file: UploadFile, file_location: str, table_name: str) -> Dict[str, Any]:
        try:
            df = pd.read_csv(file_location)
            with self.db_manager.engine.connect() as conn:
                df.to_sql(table_name, conn, if_exists='replace', index=False)

            self._store_dataset_info(table_name, file_location)

            row_count = len(df)
            return {
                "success": True,
                "message": f"CSV uploaded successfully as '{table_name}' with {row_count} rows",
                "table_name": table_name,
                "row_count": row_count,
                "columns": df.columns.tolist()
            }
        except Exception as e:
            if os.path.exists(file_location):
                os.remove(file_location)
            raise HTTPException(status_code=500, detail=f"Error uploading CSV: {str(e)}")

    def upload_excel(self, file: UploadFile, file_location: str, table_name: str) -> Dict[str, Any]:
        try:
            df = pd.read_excel(file_location, sheet_name=0)
            with self.db_manager.engine.connect() as conn:
                df.to_sql(table_name, conn, if_exists='replace', index=False)

            self._store_dataset_info(table_name, file_location)

            row_count = len(df)
            return {
                "success": True,
                "message": f"Excel uploaded successfully as '{table_name}' with {row_count} rows",
                "table_name": table_name,
                "row_count": row_count,
                "columns": df.columns.tolist()
            }
        except Exception as e:
            if os.path.exists(file_location):
                os.remove(file_location)
            raise HTTPException(status_code=500, detail=f"Error uploading Excel file: {str(e)}")

    def upload_google_sheet(self, table_name: str, url: str) -> Dict[str, Any]:
        try:
            url = url.replace("/edit?usp=sharing", "/export?format=csv")
            df = pd.read_csv(url)
            
            with self.db_manager.engine.connect() as conn:
                df.to_sql(table_name, conn, if_exists='replace', index=False)

            self._store_dataset_info(table_name, url)

            return {
                "success": True,
                "message": f"Google Sheet uploaded successfully as '{table_name}' with {len(df)} rows",
                "table_name": table_name,
                "row_count": len(df),
                "columns": df.columns.tolist()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error uploading Google Sheet: {str(e)}"
            }

    def fetch_and_update_google_sheets(self) -> Dict[str, Any]:
        datasets = self.session.query(DataSet).all()
        updated_tables = []

        for dataset in datasets:
            print(dataset.file_path)  # Debugging line
            if "docs.google.com/spreadsheets" in dataset.file_path:
                export_url = dataset.file_path.replace("/edit?usp=sharing", "/export?format=csv")
                df = pd.read_csv(export_url)

                with self.db_manager.engine.connect() as conn:
                    df.to_sql(dataset.table_name, conn, if_exists='replace', index=False)

                self.session.execute(text("UPDATE datasets SET updatedAt = :updatedAt WHERE file_path = :file_path"),
                                        {"updatedAt": datetime.now(), "file_path": dataset.file_path})
                self.session.commit()

                updated_tables.append(dataset.table_name)

        return {"success": True, "updated_tables": updated_tables}

    def get_tables(self) -> List[str]:
        return self.db_manager.get_table_names()

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        try:
            schema = self.db_manager.get_table_schema(table_name)

            if not schema:
                raise HTTPException(status_code=404, detail=f"Table '{table_name}' does not exist.")

            sample_data = self.db_manager.get_sample_data_in_rows(table_name, limit=5)

            return {
                "success": True,
                "table_name": table_name,
                "schema": schema,
                "sample_data": sample_data if sample_data else []
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting table info: {str(e)}")

    def delete_table(self, table_name: str) -> bool:
        try:
            inspector = inspect(self.db_manager.engine)
            if table_name not in inspector.get_table_names():
                return False

            with self.db_manager.engine.begin() as connection:
                connection.execute(text(f'DROP TABLE "{table_name}"'))

            dataset = self.session.query(DataSet).filter_by(table_name=table_name).first()
            if dataset:
                file_location = dataset.file_path
                self.session.delete(dataset)
                self.session.commit()

                if os.path.exists(file_location):
                    os.remove(file_location)

            return True
        except SQLAlchemyError as e:
            print(f"Error deleting table {table_name}: {str(e)}")
            return False

    def update_table_from_csv(self, table_name: str, file_location: str, replace: bool = False) -> Dict[str, Any]:
        try:
            tables = self.get_tables()
            if table_name not in tables and not replace:
                return {
                    "success": False,
                    "message": f"Table '{table_name}' does not exist. Use replace=True to create it."
                }

            df = pd.read_csv(file_location)
            with self.db_manager.engine.connect() as conn:
                if_exists = 'replace' if replace else 'append'
                df.to_sql(table_name, conn, if_exists=if_exists, index=False)

            return {
                "success": True,
                "message": f"Table '{table_name}' {'replaced' if replace else 'updated'} successfully with {len(df)} rows",
                "row_count": len(df),
                "columns": df.columns.tolist()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error updating table from CSV: {str(e)}"
            }

    def update_table_from_excel(self, table_name: str, file_location: str, replace: bool = False) -> Dict[str, Any]:
        try:
            tables = self.get_tables()
            if table_name not in tables and not replace:
                return {
                    "success": False,
                    "message": f"Table '{table_name}' does not exist. Use replace=True to create it."
                }

            # Always load the first sheet
            df = pd.read_excel(file_location, sheet_name=0)
            with self.db_manager.engine.connect() as conn:
                if_exists = 'replace' if replace else 'append'
                df.to_sql(table_name, conn, if_exists=if_exists, index=False)

            return {
                "success": True,
                "message": f"Table '{table_name}' {'replaced' if replace else 'updated'} successfully with {len(df)} rows",
                "row_count": len(df),
                "columns": df.columns.tolist()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error updating table from Excel: {str(e)}"
            }
