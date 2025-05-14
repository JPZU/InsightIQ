import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from main_router import router
from utils.i18n import set_translator

app = FastAPI()


@app.middleware("http")
async def add_locale_middleware(request: Request, call_next):

    lang = request.headers.get("accept-language", "en").split(",")[0]
    set_translator(lang)
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
