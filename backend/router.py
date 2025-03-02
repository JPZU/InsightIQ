from fastapi import APIRouter
from apps.chat.routes import router as chat_router
from apps.synthetic_data.routes import router as synthetic_data_router

router = APIRouter()
router.include_router(chat_router, prefix="/chat", tags=["chat"])
router.include_router(synthetic_data_router, prefix="/synthetic_data", tags=["synthetic_data"])
