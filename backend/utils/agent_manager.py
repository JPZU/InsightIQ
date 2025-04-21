import ast
from sqlalchemy import text
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_openai import ChatOpenAI
from utils.db_manager import DBManager
from utils.env_manager import EnvManager
from services.chat_service import ChatService


class AgentManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentManager, cls).__new__(cls)

            db_manager = DBManager()
            db = db_manager.get_connection()

            api_key = EnvManager.get_openai_api_key()

            llm = ChatOpenAI(
                model="gpt-4o-mini", openai_api_key=api_key, temperature=0.5
            )

            cls._instance._initialize(db, llm)
        return cls._instance

    def _initialize(self, db, llm):
        self.db = db
        self.agent_executor = create_sql_agent(
            llm=llm,
            db=db,
            verbose=False,
            agent_type="openai-functions",
            agent_executor_kwargs={"return_intermediate_steps": True},
            top_k=1000,
        )

    def query_nlp(self, query, chat_id=None):
        context = ""
        if chat_id:
            messages = ChatService.get_chat_messages(chat_id, limit=10)
            context = "\n".join([f"{m['type']}: {m['content']}" for m in messages])

        prompt = f"{context}\nUser: {query}" if context else query

        response = self.agent_executor.invoke({"input": prompt})
        intermediate_steps = response.get('intermediate_steps', [])

        sql_query = None
        for step in intermediate_steps:
            tool_input = step[0].tool_input if hasattr(step[0], "tool_input") else {}
            if isinstance(tool_input, dict) and "query" in tool_input:
                sql_query = tool_input["query"]
                break

        result_data = {}
        if sql_query:
            try:
                with self.db._engine.connect() as conn:
                    result = conn.execute(text(sql_query))
                    rows = result.fetchall()
                    keys = result.keys()
                    result_data = {key: [row[i] for row in rows] for i, key in enumerate(keys)}
            except Exception as e:
                result_data = {"error": str(e)}

        return {
            "output": response.get("output", ""),
            "result": result_data
        }

    def query_nlp_text_only(self, prompt):
        response = self.agent_executor.invoke({"input": prompt})
        return response.get("output", "")
