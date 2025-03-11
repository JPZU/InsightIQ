from langchain_openai import ChatOpenAI

from utils.db_manager import DBManager
from utils.env_manager import EnvManager


class SyntheticDataManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SyntheticDataManager, cls).__new__(cls)
            api_key = EnvManager.get_api_key()
            cls._instance.llm = ChatOpenAI(
                model="gpt-4o-mini", openai_api_key=api_key, temperature=0.6
            )
            cls._instance.db_manager = DBManager()
        return cls._instance

    def generate_synthetic_data(
        self,
        details: str,
        table_name: str,
        table_schema: str,
        num_records: int,
        sample_data: list = None,
    ):

        prompt = f"""
        Generate {num_records} rows of synthetic data
        based on this information: table name: {table_name}. Schema: {table_schema}.
        """

        if details:
            prompt += f"""
            Following are some details the user specified to generate the data. Fulfill their request.
            If the user makes a request in a language other than the one of the dataset,
            still adhere to the format of the CSV: '{details}'.
            """
        if sample_data:
            prompt += f" Take as a guide these real rows from the table: {sample_data}."

        prompt += " Return ONLY the data, in CSV format."

        response = self.llm.invoke(prompt)
        csv_data = response.content

        return csv_data
