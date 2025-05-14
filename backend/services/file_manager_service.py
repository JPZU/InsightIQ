import os
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect, text
from fastapi import UploadFile, HTTPException
from typing import List, Dict, Any

from utils.db_manager import DBManager


class FileManagerService:
    def __init__(self):
        self.db_manager = DBManager()

    def upload_csv(self, file: UploadFile, file_location: str, table_name: str) -> Dict[str, Any]:
        try:
            df = pd.read_csv(file_location)
            with self.db_manager.engine.connect() as conn:
                df.to_sql(table_name, conn, if_exists='replace', index=False)
            
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
        finally:
            if os.path.exists(file_location):
                os.remove(file_location)

    def upload_excel(self, file: UploadFile, file_location: str, table_name: str) -> Dict[str, Any]:
        try:
            df = pd.read_excel(file_location, sheet_name=0)
            with self.db_manager.engine.connect() as conn:
                df.to_sql(table_name, conn, if_exists='replace', index=False)
            
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
        finally:
            if os.path.exists(file_location):
                os.remove(file_location)

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
                
            return True
        except SQLAlchemyError as e:
            print(f"Error deleting table {table_name}: {str(e)}")  # For debugging
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
