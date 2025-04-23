import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from router import router
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.get("/")
def read_root():
    return {"message": "Welcome to SoftServeAnalytics API"}
