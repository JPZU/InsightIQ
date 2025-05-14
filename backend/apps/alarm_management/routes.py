from fastapi import APIRouter, HTTPException, Path, Query
import traceback

from apps.alarm_management.service import (create_alarm_from_natural_language,
                                           delete_alarm_by_id,
                                           evaluate_alarms_for_all_tables,
                                           get_all_alarms, update_alarm_by_id)
from schemas.alarm import AlarmUpdateRequest

router = APIRouter()


@router.post("/create")
def create_alarm(user_input: str = Query(..., description="Describe your alarm in natural language")):
    """
    Create an alarm from a natural language description.
    The system will automatically detect the table.
    """
    result = create_alarm_from_natural_language(user_input)
    return result


@router.delete("/delete/{alarm_id}")
def delete_alarm(alarm_id: int):
    """
    Delete an alarm by its ID.
    """
    try:
        result = delete_alarm_by_id(alarm_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
def list_alarms():
    """
    Retrieve all alarms stored in the system.
    """
    return get_all_alarms()


@router.patch("/update/{alarm_id}")
def update_alarm(
    alarm_id: int = Path(..., description="ID of the alarm to update"),
    updated_fields: AlarmUpdateRequest = ...
):
    """
    Update one or more fields of an existing alarm.
    Only include the fields you want to change. Use null to skip any field.
    """
    try:
        filtered_fields = updated_fields.dict(exclude_none=True)
        result = update_alarm_by_id(alarm_id, filtered_fields)
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/check_alarm")
def check_alarm():
    try:
        # Log para verificar si la función se está llamando
        print("Evaluando alarmas...")
        result = evaluate_alarms_for_all_tables()
        print("Resultado de evaluación:", result)
        return result
    except Exception as e:
        # Log para ver el error exacto con más detalles
        error_message = f"Error al evaluar alarmas: {str(e)}"
        print(error_message)
        print("Detalles del error:", traceback.format_exc())  # Imprime el stack trace
        raise HTTPException(status_code=500, detail=error_message)