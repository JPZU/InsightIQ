from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
import os

class DBManager:
    def __init__(self):
        db_path = os.path.abspath("data/db.sqlite")
        engine = create_engine(f"sqlite:///{db_path}")
        self.db = SQLDatabase(engine=engine)

    def get_connection(self):
        return self.db
