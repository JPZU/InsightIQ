import os

from dotenv import load_dotenv


class EnvManager:

    load_dotenv()

    @classmethod
    def get_api_key(cls):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not in .env")
        return api_key
