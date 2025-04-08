from fastapi import APIRouter, Query
from apps.alarm_management.service import create_alarm_from_natural_language

router = APIRouter()


@router.post("/create")
def create_alarm(user_input: str = Query(..., description="Describe your alarm in natural language")):
    """
    Create an alarm from a natural language description.
    The system will automatically detect the table.
    """
    result = create_alarm_from_natural_language(user_input)
    return result
