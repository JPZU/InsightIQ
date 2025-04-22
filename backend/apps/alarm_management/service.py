import json
from utils.alarm_manager import AlarmManager
from datetime import datetime


def create_alarm_from_natural_language(user_input: str):
    alarm_manager = AlarmManager()

    db_manager = alarm_manager.db_manager
    available_tables = db_manager.get_table_names()
    table_name = alarm_manager.detect_table(user_input, available_tables)

    if not table_name:
        raise ValueError("No table detected from user input.")

    schema = db_manager.get_table_schema(table_name)
    sample_data = db_manager.get_sample_data(table_name, limit=3)

    if not schema:
        raise ValueError(f"No schema found for table '{table_name}'.")

    formatted_schema = ", ".join([f"{col['column_name']} ({col['data_type']})" for col in schema])

    response = alarm_manager.generate_alarm_details(
        user_input=user_input,
        table_schema=formatted_schema,
        sample_data=sample_data
    )

    try:
        alarm_details = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("The AI response could not be parsed as JSON.")
    
    alert_data = {
        "condition": alarm_details["condition"],
        "table_name": table_name,
        "field": alarm_details["field"],
        "threshold": alarm_details["threshold"],
        "description": alarm_details["description"],
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
        "user_id": alarm_details.get("user_id", 1) 
    }

    alarm_manager.insert_alarm(alert_data)

    return {
        "message": "Alarm created successfully.",
        "table_name": table_name,
        "alarm_details": alarm_details
    }

def delete_alarm_by_id(alarm_id: int):
    alarm_manager = AlarmManager()
    alarm_manager.delete_alarm(alarm_id)
    return {
        "message": f"Alarm with ID {alarm_id} deleted successfully."
    }

def get_all_alarms():
    alarm_manager = AlarmManager()
    alarms = alarm_manager.get_all_alarms()
    return alarms

def update_alarm_by_id(alarm_id: int, updated_details: dict):
    if not updated_details:
        return {
            "success": False,
            "message": "No fields to update"
        }

    try:
        alarm_manager = AlarmManager()
        alarm_manager.edit_alarm(alarm_id, updated_details)
        return {
            "success": True,
            "message": f"Alarm {alarm_id} updated successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error updating alarm: {str(e)}"
        }

def evaluate_alarm(table_name: str):
    alarm_manager = AlarmManager()
    triggered_alarms = alarm_manager.evaluate_alarm(table_name)
    return {
        "triggered_alarms": triggered_alarms
    }