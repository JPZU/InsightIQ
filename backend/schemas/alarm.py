from typing import Optional

from pydantic import BaseModel


class AlarmUpdateRequest(BaseModel):
    table_name: Optional[str] = None
    condition: Optional[str] = None
    field: Optional[str] = None
    threshold: Optional[float] = None
    description: Optional[str] = None
