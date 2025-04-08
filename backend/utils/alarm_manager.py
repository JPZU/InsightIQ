from langchain_openai import ChatOpenAI
from utils.db_manager import DBManager
from utils.env_manager import EnvManager
from sqlalchemy.sql import text
from database.session import engine

class AlarmManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AlarmManager, cls).__new__(cls)
            api_key = EnvManager.get_api_key()
            cls._instance.llm = ChatOpenAI(
                model="gpt-4o-mini",
                openai_api_key=api_key,
                temperature=0.6
            )
            cls._instance.db_manager = DBManager()
        return cls._instance

    def detect_table(self, user_input: str, available_tables: list):
        prompt = f"""
        You are an assistant that helps identify the correct database table based on the user's natural language request.

        Available tables: {', '.join(available_tables)}.

        User input: "{user_input}"

        Respond with ONLY the table name that best fits the user's request.
        """

        response = self.llm.invoke(prompt)
        return response.content.strip()

    def generate_alarm_details(self, user_input: str, table_schema: str, sample_data: list = None):
        prompt = f"""
        Act as an assistant that helps create alarms for inventory management.
        The user will describe the alarm in natural language, and you will generate a structured alarm detail.

        Table schema: {table_schema}.

        """

        if sample_data:
            prompt += f"Here is some sample data to help you understand the context: {sample_data}.\n"

        prompt += f"""
        User request: "{user_input}"

        Provide a JSON object with the following keys:
        - 'field': the column name from the schema to monitor
        - 'condition': the condition to trigger the alarm (e.g., less than, greater than)
        - 'threshold': the numeric or text value that will trigger the alarm
        - 'description': a human-readable description of the alarm

        Return ONLY the JSON object. Do NOT include extra explanations or formatting.
        """

        response = self.llm.invoke(prompt)
        return response.content

    def insert_alarm(self, alarm_details: dict):
        query = text("""
            INSERT INTO alerts (`condition`, createdAt, updatedAt, user_id)
            VALUES (:condition, :createdAt, :updatedAt, :user_id)
        """)
        with engine.connect() as conn:
            conn.execute(query, {
                "condition": alarm_details["condition"],
                "createdAt": alarm_details["createdAt"],
                "updatedAt": alarm_details["updatedAt"],
                "user_id": alarm_details["user_id"]
            })
            conn.commit()