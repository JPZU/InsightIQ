from fastapi import APIRouter

from apps.chat.routes import router as chat_router
from apps.dashboard.routes import router as dashboard_router
from apps.file_manager.routes import router as file_manager_router
from apps.synthetic_data.routes import router as synthetic_data_router
from apps.alarm_management.routes import router as alarm_management_router

router = APIRouter()
router.include_router(chat_router, prefix="/chats", tags=["chat"])
router.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["dashboard"])
router.include_router(
    synthetic_data_router, prefix="/synthetic_data", tags=["synthetic_data"]
)
router.include_router(
    file_manager_router, prefix="/file_manager", tags=["file_manager"]
)
router.include_router(
    alarm_management_router, prefix="/alarm_management", tags=["alarm_management"]
)
