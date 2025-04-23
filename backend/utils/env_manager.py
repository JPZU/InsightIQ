import os
from dotenv import load_dotenv

from utils.i18n import _


class EnvManager:
    _initialized = False

    @classmethod
    def _ensure_initialized(cls):
        if not cls._initialized:
            load_dotenv()
            cls._initialized = True

    @classmethod
    def _get_env_var(cls, key: str) -> str:
        cls._ensure_initialized()
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Missing environment variable: {key}")
        return value

    @staticmethod
    def get_openai_api_key() -> str:
        return EnvManager._get_env_var("OPENAI_API_KEY")

    @staticmethod
    def get_database_url() -> str:
        return EnvManager._get_env_var("DATABASE_URL")

    @staticmethod
    def get_jwt_secret_key() -> str:
        return EnvManager._get_env_var("JWT_SECRET_KEY")

    @staticmethod
    def get_jwt_algorithm() -> str:
        return EnvManager._get_env_var("JWT_ALGORITHM")

    @staticmethod
    def get_jwt_expiration_time() -> int:
        return int(EnvManager._get_env_var("JWT_EXPIRATION_TIME"))
