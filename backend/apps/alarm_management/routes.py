from fastapi import APIRouter, Query, Path, HTTPException
from apps.alarm_management.service import create_alarm_from_natural_language, delete_alarm_by_id, get_all_alarms, update_alarm_by_id, evaluate_alarm
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
def check_alarm(
    table_name: str = Query(..., description="Name of the table to check alarms for"),
):
    """
    Check if any alarms are triggered based on the provided parameters.
    """
    # This function should be implemented in the service layer
    # For now, we will just return a placeholder response
    try:
        result = evaluate_alarm(table_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))