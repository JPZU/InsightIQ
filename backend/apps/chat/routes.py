from fastapi import APIRouter, HTTPException, Depends

from services.chat_service import ChatService
from utils.base_schema import BaseResponse
from utils.auth_manager import AuthManager

router = APIRouter()
chat_service = ChatService()
auth_manager = AuthManager()


@router.get("/")
def get_chats(current_user: int = Depends(auth_manager.get_current_user)):
    chats = chat_service.get_chats(current_user)
    return BaseResponse(success=True, response=[{"id": chat.id, "name": chat.name} for chat in chats])


@router.post("/")
def create_chat(name: str = "New Chat", current_user: int = Depends(auth_manager.get_current_user)):
    chat = chat_service.create_chat(current_user, name)
    return BaseResponse(success=True, response={"id": chat.id, "name": chat.name})


@router.get("/{chat_id}")
def get_chat_messages(chat_id: int, current_user: int = Depends(auth_manager.get_current_user)):
    chat = chat_service.get_chat_by_id(chat_id)
    if not chat or chat.user_id != current_user:
        raise HTTPException(status_code=404, detail="Chat not found or access denied")

    messages = chat_service.get_chat_messages(chat_id)
    return BaseResponse(success=True, response={"chat_id": chat_id, "messages": messages})


@router.delete("/{chat_id}")
def delete_chat(chat_id: int, current_user: int = Depends(auth_manager.get_current_user)):
    chat = chat_service.get_chat_by_id(chat_id)
    if not chat or chat.user_id != current_user:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this chat")

    success = chat_service.delete_chat(chat_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete chat")

    return BaseResponse(success=True, message="Chat deleted successfully")


@router.put("/{chat_id}/name")
def update_chat(chat_id: int, new_name: str, current_user: int = Depends(auth_manager.get_current_user)):
    chat = chat_service.get_chat_by_id(chat_id)
    if not chat or chat.user_id != current_user:
        raise HTTPException(status_code=403, detail="Unauthorized to update this chat")

    success = chat_service.update_chat_name(chat_id, new_name)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update chat title")

    return BaseResponse(success=True, message="Chat title updated successfully")


@router.delete("/{chat_id}/clear")
def clear_chat(chat_id: int, current_user: int = Depends(auth_manager.get_current_user)):
    chat = chat_service.get_chat_by_id(chat_id)
    if not chat or chat.user_id != current_user:
        raise HTTPException(status_code=403, detail="Unauthorized to clear messages from this chat")

    success = chat_service.clear_chat_messages(chat_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to clear chat messages")

    return BaseResponse(success=True, message="Chat messages cleared successfully")


@router.post("/{chat_id}/ask")
def ask_chat(chat_id: int, question: str, current_user: int = Depends(auth_manager.get_current_user)):
    chat = chat_service.get_chat_by_id(chat_id)
    if not chat or chat.user_id != current_user:
        raise HTTPException(status_code=403, detail="Unauthorized to ask in this chat")

    response = chat_service.ask_chat(chat_id, question)
    return BaseResponse(success=True, response={"chat_id": chat_id, "answer": response})
