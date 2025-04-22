from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):
    success: bool
    message: Optional[str] = None
    response: Optional[T] = None
