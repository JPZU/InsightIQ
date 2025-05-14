import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.chat_service import ChatService
from services.question_service import QuestionService
from services.response_service import ResponseService
from utils.agent_manager import AgentManager
from utils.auth_manager import AuthManager
from utils.base_schema import BaseResponse
from pydantic import BaseModel, conint

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
agent = AgentManager()


def get_authorized_chat(chat_id: int, user_id: int):
    try:
        chat = ChatService.get_chat_by_id(chat_id)
        if not chat or chat.user_id != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized access to this chat")
        return chat
    except Exception as e:
        logger.error(f"Error in get_authorized_chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/")
def get_chats(current_user: int = Depends(AuthManager.get_current_user)):
    try:
        chats = ChatService.get_chats(current_user)
        return BaseResponse(success=True, response=[{"id": chat.id, "name": chat.name} for chat in chats])
    except Exception as e:
        logger.error(f"Error in get_chats: {str(e)}")
        return BaseResponse(success=False, message=f"Failed to retrieve chats: {str(e)}")


class CreateChatRequest(BaseModel):
    name: str = "New Chat"


@router.post("/")
def create_chat(
    request: CreateChatRequest = None,
    name: str = None,
    current_user: int = Depends(AuthManager.get_current_user)
):
    try:
        chat_name = request.name if request else (name if name else "New Chat")

        chat = ChatService.create_chat(current_user, chat_name)
        return BaseResponse(success=True, response={"id": chat.id, "name": chat.name})
    except Exception as e:
        logger.error(f"Error in create_chat: {str(e)}")
        return BaseResponse(success=False, message=f"Failed to create chat: {str(e)}")


@router.get("/{chat_id}")
def get_chat_messages(chat_id: int, current_user: int = Depends(AuthManager.get_current_user)):
    try:
        get_authorized_chat(chat_id, current_user)
        messages = ChatService.get_chat_messages(chat_id)
        return BaseResponse(success=True, response={"chat_id": chat_id, "messages": messages})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in get_chat_messages: {str(e)}")
        return BaseResponse(success=False, message=f"Failed to retrieve chat messages: {str(e)}")


class ChatQuestionRequest(BaseModel):
    question: str


class ResultData(BaseModel):
    output: str
    result: Optional[Dict[str, Any]] = None
    sql_query: Optional[str] = None
    intermediate_steps: Optional[list] = None


@router.post("/{chat_id}")
def ask_chat(
    chat_id: int,
    request: ChatQuestionRequest,
    current_user: int = Depends(AuthManager.get_current_user)
):

    get_authorized_chat(chat_id, current_user)

    agent_response = agent.query_nlp(request.question, chat_id)
    content = agent_response.get("content", "")
    query_result = agent_response.get("query_result", {})

    new_question = QuestionService.create_question(chat_id, request.question)
    response = ResponseService.create_response(
        chat_id=chat_id,
        question_id=new_question.id,
        content=content,
        query_result=query_result
    )

    return BaseResponse(
        success=True,
        response={
            "content": content,
            "query_result": query_result,
            "response_id": response.id  # <- esto es CLAVE
        }
    )


@router.put("/{chat_id}")
def update_chat(chat_id: int, new_name: str, current_user: int = Depends(AuthManager.get_current_user)):
    try:
        get_authorized_chat(chat_id, current_user)
        success = ChatService.update_chat_name(chat_id, new_name)
        if not success:
            return BaseResponse(success=False, message="Failed to update chat title")
        return BaseResponse(success=True, message="Chat title updated successfully")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in update_chat: {str(e)}")
        return BaseResponse(success=False, message=f"Failed to update chat: {str(e)}")


@router.delete("/{chat_id}")
def delete_chat(chat_id: int, current_user: int = Depends(AuthManager.get_current_user)):
    try:
        get_authorized_chat(chat_id, current_user)
        success = ChatService.delete_chat(chat_id)
        if not success:
            return BaseResponse(success=False, message="Failed to delete chat")
        return BaseResponse(success=True, message="Chat deleted successfully")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in delete_chat: {str(e)}")
        return BaseResponse(success=False, message=f"Failed to delete chat: {str(e)}")


@router.delete("/{chat_id}/clear")
def clear_chat(chat_id: int, current_user: int = Depends(AuthManager.get_current_user)):
    try:
        get_authorized_chat(chat_id, current_user)
        success = ChatService.clear_chat_messages(chat_id)
        if not success:
            return BaseResponse(success=False, message="Failed to clear chat messages")
        return BaseResponse(success=True, message="Chat messages cleared successfully")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in clear_chat: {str(e)}")
        return BaseResponse(success=False, message=f"Failed to clear chat messages: {str(e)}")


class RatingRequest(BaseModel):
    rating: conint(ge=0, le=1)


@router.post("/responses/{response_id}/rate")
def rate_response(
    response_id: int,
    request: RatingRequest,  # Pydantic model con campo `rating: conint(ge=0, le=1)`
    current_user: int = Depends(AuthManager.get_current_user)
):
    try:
        ResponseService.rate_response(response_id, request.rating)
        return BaseResponse(success=True, message="Rating submitted successfully")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected error rating response: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
