import csv
import io

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
                model="gpt-4o-mini",
                openai_api_key=api_key,
                temperature=0.6
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
        Generate exactly {num_records} rows of synthetic data
        based on this information: table name: {table_name}. Schema: {table_schema}.
        """

        if details:
            prompt += f"""
            Be creative but adhere to the schema.
            Following are some user specified requirements,
            Fulfill their request adhering to the format: '{details}'.
            """
        if sample_data:
            prompt += f" Take as a guide these real rows from the table: {sample_data}."

        prompt += """ Return ONLY the data in CSV format. Make sure:
        - The FIRST row contains the column headers.
        - Do NOT wrap the CSV in Markdown formatting (no triple backticks).
        - Do NOT include extra text before or after the CSV output."""

        response = self.llm.invoke(prompt)

        return response.content

    def format_data(self, response):
        csv_data = response.strip()

        if csv_data.startswith("```") and csv_data.endswith("```"):
            csv_data = csv_data[3:-3].strip()

        reader = csv.reader(io.StringIO(csv_data))
        rows = list(reader)

        if not rows or len(rows) < 2:
            print("ERROR: No valid CSV data parsed")
            return []

        headers = rows[0]
        structured_data = [
            {headers[i]: row[i].strip().strip('"') for i in range(len(headers))}
            for row in rows[1:]
        ]

        return structured_data
