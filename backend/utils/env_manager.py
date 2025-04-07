import os
from dotenv import load_dotenv


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

    @classmethod
    def get_openai_api_key(cls) -> str:
        return cls._get_env_var("OPENAI_API_KEY")

    @classmethod
    def get_database_url(cls) -> str:
        return cls._get_env_var("DATABASE_URL")

    @classmethod
    def get_jwt_secret_key(cls) -> str:
        return cls._get_env_var("JWT_SECRET_KEY")

    @classmethod
    def get_jwt_algorithm(cls) -> str:
        return cls._get_env_var("JWT_ALGORITHM")

    @classmethod
    def get_jwt_expiration_time(cls) -> int:
        return int(cls._get_env_var("JWT_EXPIRATION_TIME"))
