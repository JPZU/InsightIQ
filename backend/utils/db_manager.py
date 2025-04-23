import os

import pandas as pd
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from utils.i18n import _ 


class DBManager:
    def __init__(self):
        db_path = os.path.abspath("data/db.sqlite")
        self.data_dir = os.path.abspath("data")
        engine = create_engine(f"sqlite:///{db_path}")
        self.engine = engine
        self.db = SQLDatabase(engine=self.engine)

    def get_connection(self):
        return self.db

    def get_table_names(self):
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        with self.engine.connect() as conn:
            result = conn.execute(text(query)).fetchall()
        return [row[0] for row in result]

    def get_sample_data(self, table_name: str, limit: int):
        query = text(f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT {limit}")
        with self.engine.connect() as conn:
            result = conn.execute(query).fetchall()

        return [dict(row._mapping) for row in result] if result else None

    def get_table_schema(self, table_name: str):
        query = text(f"PRAGMA table_info({table_name})")
        with self.engine.connect() as conn:
            result = conn.execute(query).fetchall()

        if not result:
            return None

        schema = []
        for row in result:
            schema.append(
                {
                    "column_name": row[1],
                    "data_type": row[2],
                    "nullable": row[3] == 1,
                    "primary_key": row[5] == 1,
                }
            )

        return schema

    def get_dataframe(self):
        allowed_extensions = (".csv", ".xlsx")
        files = [f for f in os.listdir(
            self.data_dir) if f.endswith(allowed_extensions)]

        if not files:
            raise FileNotFoundError(_("error_no_csv_xlsx_found"))

        file_name = files[0]
        file_path = os.path.join(self.data_dir, file_name)

        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            raise ValueError(_("error_unsupported_file_format"))
        return df, file_name

    def get_all_data_from_table(self, table_name: str):
        query = text(f"SELECT * FROM {table_name}")
        with self.engine.connect() as conn:
            result = conn.execute(query).fetchall()
        return [dict(row._mapping) for row in result] if result else None
