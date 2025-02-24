from utils.agent_manager import AgentManager

class ChatService:
    sql_agent = AgentManager()

    @staticmethod
    def get_response(question: str) -> str:
        return ChatService.sql_agent.query_nlp(question)