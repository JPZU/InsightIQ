from langchain_openai import ChatOpenAI
from utils.env_manager import EnvManager
from utils.db_manager import DBManager
import pandas as pd

class SyntheticDataManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SyntheticDataManager, cls).__new__(cls)
            api_key = EnvManager.get_api_key()
            cls._instance.llm = ChatOpenAI(
                model="gpt-4o-mini",
                openai_api_key=api_key,
                temperature=0.7
            )
            cls._instance.db_manager = DBManager()
        return cls._instance


    def generate_synthetic_data(self,  table_name: str, table_schema: str, num_records: int = 10, sample_data: list=None):
        
        prompt = f"Generate {num_records} rows of synthetic data based on this table schema: {table_schema}."
        
        if sample_data:
            prompt += f" Take as a guide these real rows from the table: {sample_data}."

        prompt += " Return only the data in CSV format."

        response = self.llm.invoke(prompt)  
        csv_data = response.content 

        return csv_data 
