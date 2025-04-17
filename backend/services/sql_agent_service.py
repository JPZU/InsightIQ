from utils.agent_manager import AgentManager


class SQLAgentService:
    sql_agent = AgentManager()

    @staticmethod
    def get_response(question: str) -> dict:
        return SQLAgentService.sql_agent.query_nlp(question)
