from fastapi import APIRouter, HTTPException
from apps.chat.service import ChatService
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/")
def question(request: ChatRequest):

    response = ChatService.get_response(request.question)

    if not response:
        raise HTTPException(status_code=500, detail="Failed to process SQL query")
    return {"response": response}
