from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
import os
from sqlalchemy.sql import text

class DBManager:
    def __init__(self):
        db_path = os.path.abspath("data/db.sqlite")
        engine = create_engine(f"sqlite:///{db_path}")
        self.db = SQLDatabase(engine=engine)
        self.engine = engine

    def get_connection(self):
        return self.db
    
    
    def get_table_names(self):
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        with self.engine.connect() as conn:
            result = conn.execute(text(query)).fetchall()
        return [row[0] for row in result]
    
    
    def get_sample_data(self, table_name: str, limit: int):
        query = text(f"SELECT * FROM {table_name} LIMIT {limit}")
        with self.engine.connect() as conn:
            result = conn.execute(query, {"limit": limit}).fetchall()

        return [dict(row._mapping) for row in result] if result else None

    
    def get_table_schema(self, table_name: str):
        query = text(f"PRAGMA table_info({table_name})")
        with self.engine.connect() as conn:
            result = conn.execute(query).fetchall()

        if not result:
            return None 

        schema = []
        for row in result:
            schema.append({
                "column_name": row[1],
                "data_type": row[2],
                "nullable": row[3] == 1,
                "primary_key": row[5] == 1
            })

        return schema
