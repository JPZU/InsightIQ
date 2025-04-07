import gettext
import os
import contextvars
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALE_PATH = os.path.join(BASE_DIR, "../locales")
_current_translator = contextvars.ContextVar("current_translator", default=gettext.NullTranslations())

def set_translator(lang: str):
    try:
        translator = gettext.translation("messages", localedir=LOCALE_PATH, languages=[lang])
    except FileNotFoundError:
        translator = gettext.NullTranslations()
    _current_translator.set(translator)  
    translator.install()

def get_translator(lang: str):
    try:
        return gettext.translation("messages", localedir=LOCALE_PATH, languages=[lang])
    except FileNotFoundError:
        return gettext.NullTranslations()

def _(message: str) -> str:
    return _current_translator.get().gettext(message) 

class LanguageMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        lang = request.headers.get("accept-language", "en")
        set_translator(lang)  
        response = await call_next(request)
        return response
