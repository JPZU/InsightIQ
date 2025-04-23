from fastapi import APIRouter, HTTPException
from typing import Optional

from services.chat_service import ChatService
from utils.base_schema import BaseResponse

router = APIRouter()
chat_service = ChatService()

@router.get("/{user_id}")
def get_chats(user_id: int):
    chats = chat_service.get_chats(user_id)
    return BaseResponse(success=True, response=[{"id": chat.id, "name": chat.name} for chat in chats])

@router.post("/{user_id}")
def create_chat(user_id: int, name: str):
    chat = chat_service.create_chat(user_id, name)
    return BaseResponse(success=True, response={"id": chat.id, "name": chat.name})

@router.get("/{user_id}/{chat_id}")
def get_chat_messages(user_id: int, chat_id: int, start_message: Optional[int] = 0, end_message: Optional[int] = 20):
    chat = chat_service.get_chat_by_id(chat_id)
    if not chat or chat.user_id != user_id:
        raise HTTPException(status_code=404, detail="Chat not found or access denied")
    
    messages = chat_service.get_chat_messages(chat_id, start_message, end_message)
    return BaseResponse(success=True, response={"chat_id": chat_id, "messages": messages})

@router.delete("/{user_id}/{chat_id}")
def delete_chat(user_id: int, chat_id: int):
    chat = chat_service.get_chat_by_id(chat_id)
    if not chat or chat.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this chat")

    success = chat_service.delete_chat(chat_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete chat")
    
    return BaseResponse(success=True, message="Chat deleted successfully")

@router.put("/{user_id}/{chat_id}/name")
def update_chat(user_id: int, chat_id: int, new_name: str):
    chat = chat_service.get_chat_by_id(chat_id)
    if not chat or chat.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to update this chat")

    success = chat_service.update_chat_name(chat_id, new_name)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update chat title")

    return BaseResponse(success=True, message="Chat title updated successfully")

@router.delete("/{user_id}/{chat_id}/clear")
def clear_chat(user_id: int, chat_id: int):
    chat = chat_service.get_chat_by_id(chat_id)
    if not chat or chat.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to clear messages from this chat")

    success = chat_service.clear_chat_messages(chat_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to clear chat messages")

    return BaseResponse(success=True, message="Chat messages cleared successfully")

@router.post("/{user_id}/{chat_id}/ask")
def ask_chat(user_id: int, chat_id: int, question: str):
    chat = chat_service.get_chat_by_id(chat_id)
    if not chat or chat.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to ask in this chat")

    response = chat_service.ask_chat(chat_id, question)
    return BaseResponse(success=True, response={"chat_id": chat_id, "answer": response})
