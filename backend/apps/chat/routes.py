from fastapi import APIRouter, HTTPException, Depends
from services.chat_service import ChatService
from services.question_service import QuestionService
from services.response_service import ResponseService
from utils.agent_manager import AgentManager
from utils.auth_manager import AuthManager
from utils.base_schema import BaseResponse

router = APIRouter()
agent = AgentManager() 


def get_authorized_chat(chat_id: int, user_id: int):
    chat = ChatService.get_chat_by_id(chat_id)
    if not chat or chat.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access to this chat")
    return chat


@router.get("/")
def get_chats(current_user: int = Depends(AuthManager.get_current_user)):
    chats = ChatService.get_chats(current_user)
    return BaseResponse(success=True, response=[{"id": chat.id, "name": chat.name} for chat in chats])


@router.post("/")
def create_chat(name: str = "New Chat", current_user: int = Depends(AuthManager.get_current_user)):
    chat = ChatService.create_chat(current_user, name)
    return BaseResponse(success=True, response={"id": chat.id, "name": chat.name})


@router.get("/{chat_id}")
def get_chat_messages(chat_id: int, current_user: int = Depends(AuthManager.get_current_user)):
    get_authorized_chat(chat_id, current_user)
    messages = ChatService.get_chat_messages(chat_id)
    return BaseResponse(success=True, response={"chat_id": chat_id, "messages": messages})


@router.post("/{chat_id}")
def ask_chat(chat_id: int, question: str, current_user: int = Depends(AuthManager.get_current_user)):
    get_authorized_chat(chat_id, current_user)

    agent_response = agent.query_nlp(question, chat_id)
    response_text = agent_response.get("output", "")
    result_data = agent_response.get("result", {})

    new_question = QuestionService.create_question(chat_id, question)
    ResponseService.create_response(chat_id, new_question.id, response_text)

    return BaseResponse(success=True, response={
        "answer": response_text,
        "result": result_data
    })


@router.put("/{chat_id}")
def update_chat(chat_id: int, new_name: str, current_user: int = Depends(AuthManager.get_current_user)):
    get_authorized_chat(chat_id, current_user)
    success = ChatService.update_chat_name(chat_id, new_name)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update chat title")
    return BaseResponse(success=True, message="Chat title updated successfully")


@router.delete("/{chat_id}")
def delete_chat(chat_id: int, current_user: int = Depends(AuthManager.get_current_user)):
    get_authorized_chat(chat_id, current_user)
    success = ChatService.delete_chat(chat_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete chat")
    return BaseResponse(success=True, message="Chat deleted successfully")


@router.delete("/{chat_id}/clear")
def clear_chat(chat_id: int, current_user: int = Depends(AuthManager.get_current_user)):
    get_authorized_chat(chat_id, current_user)
    success = ChatService.clear_chat_messages(chat_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to clear chat messages")
    return BaseResponse(success=True, message="Chat messages cleared successfully")
