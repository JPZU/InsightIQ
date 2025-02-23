import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

class LangChainManager:
    _instance = None
    
    def __init__(self):
        if LangChainManager._instance is None:
            LangChainManager._instance = self
            self._initialize_model()
        else:
            raise Exception("This class is a singleton! Use get_instance() instead.")
    
    def _initialize_model(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
        
        self.model = init_chat_model("gpt-4o-mini", model_provider="openai")
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = LangChainManager()
        return cls._instance
    
    def get_response(self, message: str) -> str:
        response = self.model.invoke(message)
        return response