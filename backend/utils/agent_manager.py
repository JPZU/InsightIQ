from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from utils.env_manager import EnvManager
from utils.db_manager import DBManager

class AgentManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentManager, cls).__new__(cls)

            db_manager = DBManager()
            db = db_manager.get_connection()

            api_key = EnvManager.get_api_key()

            llm = ChatOpenAI(
                model="gpt-4o-mini",
                openai_api_key=api_key,
                temperature=0.2
            )

            cls._instance._initialize(db, llm)
        return cls._instance

    def _initialize(self, db, llm):
        self.agent_executor = create_sql_agent(
            llm=llm,
            db=db,
            verbose=False,
            agent_type="openai-functions",
            agent_executor_kwargs={"return_intermediate_steps": True},
            top_k=1000
        )

    def query_nlp(self, query):
        response = self.agent_executor.invoke({"input": query})

        return {
            'input': response.get('input', ''),
            'output': response.get('output', ''),
            'query': response.get('intermediate_steps')[3][0].tool_input['query'],
            'query_output': response.get('intermediate_steps')[3][1]
        }
