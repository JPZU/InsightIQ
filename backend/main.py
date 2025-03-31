from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import gettext
import os

from router import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
def read_root():
    return {"message": "Welcome to SoftServeAnalytics API"}


def get_translator(language: str):
    locale_path = os.path.join(BASE_DIR, "locales")
    try:
        return gettext.translation('messages', localedir=locale_path, languages=[language])
    except FileNotFoundError:
        return gettext.NullTranslations()

@app.get("/greet/")
async def greet(request: Request, lang: str = "en"):
    translator = get_translator(lang)
    translator.install()
    _ = translator.gettext

    return {"message": _("welcome_message")}
