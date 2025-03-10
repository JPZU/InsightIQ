from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from utils.env_manager import EnvManager
from utils.db_manager import DBManager
import ast

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
                temperature=0.5
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
        intermediate_steps = response.get('intermediate_steps', [])
        print(intermediate_steps[1][1])


        if len(intermediate_steps) > 3:
            query = intermediate_steps[3][0].tool_input['query']
            query_output = intermediate_steps[3][1]
        else:
            intermediate_query = intermediate_steps[1][1].split('/*')

            query = intermediate_query[0]
            query_output = intermediate_query[1][28:-3].replace('\t', ';').split('\n')
        
        x_axis = []
        y_axis = []

        if isinstance(query_output, str) and query_output.startswith('[') and query_output.endswith(']'):
            try:
                query_output = ast.literal_eval(query_output)
            except (ValueError, SyntaxError):
                pass

        if isinstance(query_output, list):
            for item in query_output:
                if isinstance(item, (tuple, list)) and len(item) == 2:
                    x_axis.append(str(item[0]))
                    y_axis.append(item[1])

        return {
            'input': response.get('input', ''),
            'output': response.get('output', ''),
            'query': query,
            'query_output': query_output,
            'x_axis': x_axis,
            'y_axis': y_axis
        }

