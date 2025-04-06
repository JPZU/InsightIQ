import asyncio
from functools import partial

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from apps.chat.service import ChatService

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/")
async def question(request: ChatRequest):
    try:
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(None, partial(ChatService.get_response, request.question)),
            timeout=30.0
        )

        if not response:
            raise HTTPException(
                status_code=500,
                detail="Failed to process SQL query")

        return {"response": response}

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=503,
            detail="Server is busy or not connected. Please try again later."
        )
