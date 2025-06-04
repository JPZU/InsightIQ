from datetime import datetime
from typing import Dict, List, Set, Tuple

from langchain_openai import ChatOpenAI
from sqlalchemy.sql import text

from database.session import engine
from utils.db_manager import DBManager
from utils.env_manager import EnvManager


class AlarmManager:
    _instance = None
    db_manager: DBManager
    _alarm_history: Dict[Tuple[str, int], Set[Tuple]]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AlarmManager, cls).__new__(cls)
            cls._instance.db_manager = DBManager()
            cls._instance._alarm_history = {}

            api_key = EnvManager.get_openai_api_key()
            cls._instance.llm = ChatOpenAI(
                model="gpt-4o-mini",
                openai_api_key=api_key,
                temperature=0.6
            )
        return cls._instance

    def _get_history_key(self, table_name: str, alarm_id: int) -> Tuple[str, int]:
        """Generate a consistent key for history tracking."""
        return (table_name, alarm_id)

    def _get_triggered_data_key(self, triggered_data: dict) -> Tuple:
        """Create a hashable key from triggered data for history tracking."""
        return tuple(sorted((k, str(v)) for k, v in triggered_data.items()))

    def _filter_new_alarms(self, table_name: str, alarm_id: int, triggered_rows: List[dict]) -> List[dict]:
        """Filter out alarms that are already in history."""
        history_key = self._get_history_key(table_name, alarm_id)
        existing_alarms = self._alarm_history.get(history_key, set())

        new_alarms = []
        for row in triggered_rows:
            data_key = self._get_triggered_data_key(row['triggered_data'])
            if data_key not in existing_alarms:
                new_alarms.append(row)
        return new_alarms

    def _update_history(self, table_name: str, alarm_id: int, triggered_rows: List[dict]):
        """Update history with newly triggered alarms."""
        history_key = self._get_history_key(table_name, alarm_id)
        if history_key not in self._alarm_history:
            self._alarm_history[history_key] = set()

        for row in triggered_rows:
            data_key = self._get_triggered_data_key(row['triggered_data'])
            self._alarm_history[history_key].add(data_key)

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

        is_active = alarm_details.get("is_active", True)

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

    def evaluate_alarm(self, table_name: str, only_new: bool = True) -> List[dict]:
        """
        Evaluate alarms for a table and return triggered alarms.
        """
        query = text("""SELECT * FROM alerts where table_name = :table_name AND is_active = 1""")
        results_triggered = []

        try:
            with engine.connect() as conn:
                result = conn.execute(query, {"table_name": table_name})
                alarms = result.mappings().all()

                for alarm in alarms:
                    condition = alarm.get("condition")
                    if condition is None:
                        print(f"Alarma {alarm['id']} no tiene condición definida.")
                        continue  # Salta si la condición no está definida
                    else:
                        print(f"Alarma {alarm['id']} con condición: {condition}")

                    field = alarm["field"]
                    threshold = alarm["threshold"]
                    alarm_id = alarm["id"]

                    if condition == "less than":
                        cond_sql = f'"{field}" < {threshold}'
                    elif condition == "greater than":
                        cond_sql = f'"{field}" > {threshold}'
                    elif condition == "equal to":
                        cond_sql = f'"{field}" = {threshold}'
                    else:
                        print(f"Condición no válida para la alarma {alarm['id']}")
                        continue

                    check_query = text(f"SELECT * FROM {table_name} WHERE {cond_sql}")
                    with self.db_manager.engine.connect() as conn:
                        triggered = conn.execute(check_query).mappings().all()

                        if triggered:
                            triggered_rows = [{
                                "alarm_id": alarm_id,
                                "description": alarm["description"],
                                "triggered_data": dict(row)
                            } for row in triggered]

                            if only_new:
                                triggered_rows = self._filter_new_alarms(table_name, alarm_id, triggered_rows)

                            if triggered_rows:
                                results_triggered.extend(triggered_rows)
                                self._update_history(table_name, alarm_id, triggered_rows)

        except Exception as e:
            raise e  # Puedes volver a lanzar el error si quieres que se propague

        return results_triggered

    def clear_history(self, table_name: str = None, alarm_id: int = None):
        """Clear history for specific table/alarm or all history."""
        if table_name is None and alarm_id is None:
            self._alarm_history.clear()
        else:
            keys_to_remove = [
                key for key in self._alarm_history.keys()
                if (table_name is None or key[0] == table_name)
                and (alarm_id is None or key[1] == alarm_id)
            ]
            for key in keys_to_remove:
                del self._alarm_history[key]

    def delete_alarm(self, alarm_id: int):
        query = text("DELETE FROM alerts WHERE id = :alarm_id")
        with engine.connect() as conn:
            conn.execute(query, {"alarm_id": alarm_id})
            conn.commit()
        self.clear_history(alarm_id=alarm_id)

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
