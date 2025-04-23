from langchain_openai import ChatOpenAI
from utils.db_manager import DBManager
from utils.env_manager import EnvManager
from sqlalchemy.sql import text
from datetime import datetime
from database.session import engine

class AlarmManager:
    _instance = None
    db_manager: DBManager

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
            INSERT INTO alerts (`condition`, `table_name`, `field`, `threshold`, `description`, createdAt, updatedAt, user_id, is_active)
            VALUES (:condition, :table_name, :field, :threshold, :description, :createdAt, :updatedAt, :user_id, :is_active)
        """)
        
        is_active = alarm_details.get("is_active", True)  # By default, set to True
        
        with engine.connect() as conn:
            conn.execute(query, {
                "condition": alarm_details["condition"],
                "table_name": alarm_details["table_name"],
                "field": alarm_details["field"],
                "threshold": alarm_details["threshold"],
                "description": alarm_details["description"],
                "createdAt": alarm_details["createdAt"],
                "updatedAt": alarm_details["updatedAt"],
                "user_id": alarm_details["user_id"],
                "is_active": is_active  
            })
            conn.commit()
            
    def evaluate_alarm(self, table_name: str):
        query = text("""
            SELECT * FROM alerts where table_name = :table_name AND is_active = 1
        """)
        results_triggered = []

        with engine.connect() as conn:
            result = conn.execute(query, {"table_name": table_name})
            alarms = result.mappings().all()
            
            for alarm in alarms:
                field = alarm["field"]
                condition = alarm["condition"]
                threshold = alarm["threshold"]

                if condition == "less than":
                    cond_sql = f'"{field}" < {threshold}'
                elif condition == "greater than":
                    cond_sql = f'"{field}" > {threshold}'
                elif condition == "equal to":
                    cond_sql = f'"{field}" = {threshold}'
                else:
                    continue  # Skip unknown conditions

                check_query = text(f"SELECT * FROM {table_name} WHERE {cond_sql}")
                with self.db_manager.engine.connect() as conn:
                    triggered = conn.execute(check_query).mappings().all()

                    if triggered:
                        for row in triggered:
                            results_triggered.append({
                                "alarm_id": alarm["id"],
                                "description": alarm["description"],
                                "triggered_data": dict(row)
                            })
        return results_triggered
    
    def delete_alarm(self, alarm_id: int):
        query = text("DELETE FROM alerts WHERE id = :alarm_id")
        with engine.connect() as conn:
            conn.execute(query, {"alarm_id": alarm_id})
            conn.commit()

    def get_all_alarms(self):
        query = text("SELECT * FROM alerts")
        with engine.connect() as conn:
            result = conn.execute(query).mappings().all()
            return [dict(row) for row in result]

    def edit_alarm(self, alarm_id: int, updated_details: dict):
        if not updated_details:
            return  

        updated_details["updatedAt"] = datetime.utcnow().isoformat()

        set_clauses = []
        params = {"alarm_id": alarm_id}

        for key, value in updated_details.items():
            set_clauses.append(f"`{key}` = :{key}")
            params[key] = value

        set_clause = ", ".join(set_clauses)

        query = text(f"""
            UPDATE alerts
            SET {set_clause}
            WHERE id = :alarm_id
        """)

        with engine.connect() as conn:
            conn.execute(query, params)
            conn.commit()