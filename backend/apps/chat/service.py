from utils.agent_manager import AgentManager









class ChatService:
    sql_agent = AgentManager()

    @staticmethod
    def get_response(question: str) -> dict:
        return ChatService.sql_agent.query_nlp(question)
