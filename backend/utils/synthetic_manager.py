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
                temperature=0.6
            )
            cls._instance.db_manager = DBManager()
        return cls._instance


    def generate_synthetic_data(self,  details: str, table_name: str, table_schema: str, num_records: int = 10, sample_data: list=None):
        
        prompt = f"For a table called '{table_name}', generate {num_records} rows of synthetic data based on this schema: {table_schema}."
        
        if details:
            prompt += f" Here are some details specified to generate the data: {details}."
        if sample_data:
            prompt += f" Take as a guide these real rows from the table: {sample_data}."

        prompt += " Return ONLY the data, in CSV format."

        response = self.llm.invoke(prompt)  
        csv_data = response.content 

        return csv_data 
