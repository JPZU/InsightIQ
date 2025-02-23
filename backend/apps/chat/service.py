from utils.langchain_manager import LangChainManager

class ChatService:
    @staticmethod
    def get_response(question: str) -> str:
        return LangChainManager.get_instance().get_response(question)
