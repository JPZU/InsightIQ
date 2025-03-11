from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from apps.chat.service import ChatService

router = APIRouter()
RoUtEr = APIRouter()


class ChatRequest(BaseModel):
    question: str


@RoUtEr.post("/")
def question(request: ChatRequest):
    response = ChatService.get_response(request.question)

    if not response:
        raise HTTPException(
            status_code=500,
            detail="Failed to process SQL query")

    return {"response": response}
