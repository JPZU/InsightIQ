from fastapi import APIRouter
from apps.chat.routes import router as chat_router
from apps.file_manager.routes import router as file_manager_router

router = APIRouter()
router.include_router(chat_router, prefix="/chat", tags=["chat"])
router.include_router(file_manager_router, prefix="/file_manager", tags=["file_manager"])
