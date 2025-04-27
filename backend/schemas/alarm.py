from pydantic import BaseModel
from typing import Optional

class AlarmUpdateRequest(BaseModel):
    table_name: Optional[str] = None
    condition: Optional[str] = None
    field: Optional[str] = None
    threshold: Optional[float] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
