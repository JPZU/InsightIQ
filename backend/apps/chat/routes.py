import asyncio
from functools import partial
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from flask_babel import gettext as _

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
                detail=_("error_sql_processing_failed"))

        return {"response": response}

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=503,
            detail=_("error_server_busy")
        )
