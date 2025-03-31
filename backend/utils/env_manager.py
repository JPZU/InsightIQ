import os

from dotenv import load_dotenv
from flask_babel import gettext as _

class EnvManager:

    load_dotenv()

    @classmethod
    def get_api_key(cls):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(_("error_openai_api_key_missing"))
        return api_key
