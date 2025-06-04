from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_openai import ChatOpenAI
from sqlalchemy import text
from services.chat_service import ChatService
from utils.db_manager import DBManager
from utils.env_manager import EnvManager
from typing import List, Dict, Any
import asyncio


class AgentManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentManager, cls).__new__(cls)
            db_manager = DBManager()
            llm = ChatOpenAI(
                model="gpt-4o-mini",
                openai_api_key=EnvManager.get_openai_api_key(),
                temperature=0.6,  # Lower temperature for more consistent results
                max_tokens=400,  # Limit token usage
                request_timeout=30  # Add timeout
            )
            cls._instance._initialize(db_manager.get_connection(), llm)
        return cls._instance

    def _initialize(self, db, llm):
        self.db = db
        self.agent_executor = create_sql_agent(
            llm=llm,
            db=db,
            verbose=False,
            agent_type="openai-functions",
            agent_executor_kwargs={
                "return_intermediate_steps": True,
                "handle_parsing_errors": True,  # Add this to handle parsing errors
            },
            top_k=500,  # Reduced from 1000 to improve performance
        )

    def _validate_sql_query(self, query: str) -> str:
        """Validate and fix common SQL query issues."""
        if not query:
            return query
            
        # Remove any trailing commas
        query = query.rstrip(',')
        
        # Ensure the query ends with a semicolon
        if not query.rstrip().endswith(';'):
            query = query.rstrip() + ';'
            
        # Fix common syntax errors
        query = query.replace('SELECT SELECT', 'SELECT')  # Fix double SELECT
        query = query.replace('FROM FROM', 'FROM')        # Fix double FROM
        query = query.replace('WHERE WHERE', 'WHERE')     # Fix double WHERE
        
        # Ensure proper quoting for column names with spaces
        for col in ["Stock actual", "Precio unitario", "Fecha de entrada", "Fecha de salida", 
                   "nombre", "ventas", "faltas"]:
            if col in query and f'"{col}"' not in query:
                query = query.replace(col, f'"{col}"')
        
        return query

    async def _process_single_query(self, query: str, chat_id: str = None) -> Dict[str, Any]:
        context = ""
        if chat_id:
            messages = ChatService.get_chat_messages(chat_id, limit=5)
            context = "\n".join([f"{m['type']}: {m['content']}" for m in messages])

        # Add comprehensive instructions for different types of queries
        format_instruction = """IMPORTANT INSTRUCTIONS:

1. For Data Visualization:
   - For tables, format the response as follows:
     [Brief description of what the table shows and its significance]
     [List of data as a resume of the table]

    DONT CREATE A TABLE, JUST RETURN THE DATA AS A LIST OF DATA

     **Key Insights:**
     • [Most important observation from the data]
     • [Second most important observation if relevant]
    
   - Frontend will handle visualization

2. For SQL Queries:
   - Ensure proper syntax with correct parentheses and semicolons
   - Use double quotes for column names with spaces
   - Include ORDER BY clauses for meaningful sorting

3. For Analytical/Decision Making Queries (like performance analysis, layoffs, etc.):
   Format the response using markdown-style formatting:
   
   **Analysis:**
   • [Most important metric with specific numbers]
   • [Second most important metric if relevant]
   
   **Context:**
   [Brief explanation of why these metrics matter]
   
   **Alternative Considerations:**
   • [One key alternative to consider]
   • MAX 3 alternatives
   
4. General Guidelines:
   - Use markdown formatting for better readability
   - Be precise and data-driven
   - Provide context for recommendations
   - Consider both short-term and long-term implications
   - Acknowledge limitations in the data or analysis
   - Use bullet points (•) for lists
   - Use bold (**) for section headers
   - Use italics (*) for subsections
   - Dont use # for section headers
   - When showing multiple items, focus on the top 1-2 and mention others only if critical
   """

        prompt = f"{format_instruction}\n\nContext from previous messages:\n{context}\n\nUser Query: {query}" if context else f"{format_instruction}\n\nUser Query: {query}"
        
        try:
            response = self.agent_executor.invoke({"input": prompt})
        except Exception as e:
            error_msg = str(e)
            return {
                "content": "I apologize, but I encountered an error while processing your request. Please try rephrasing your question.",
                "query_result": {"error": "Agent execution error", "details": error_msg},
                "x_axis": [],
                "y_axis": [],
                "chartTitle": "Error in Query"
            }
        
        sql_query = None
        for step in response.get('intermediate_steps', []):
            tool_input = step[0].tool_input if hasattr(step[0], "tool_input") else {}
            if isinstance(tool_input, dict) and "query" in tool_input:
                sql_query = self._validate_sql_query(tool_input["query"])
                break

        if not sql_query:
            return {"content": response.get("output", ""), "query_result": {}}

        try:
            with self.db._engine.connect() as conn:
                result = conn.execute(text(sql_query))
                rows = result.fetchall()
                result_data = {key: [row[i] for row in rows] for i, key in enumerate(result.keys())}
                
                # Check if this is a graph request
                is_graph_request = any(word in query.lower() for word in ['gráfico', 'grafico', 'gráfica', 'grafica', 'chart', 'graph', 'visualizar', 'visualización'])
                
                if is_graph_request and len(result_data) > 2:
                    # Find text and numeric columns for the graph
                    text_column = None
                    numeric_column = None
                    
                    for col, values in result_data.items():
                        # Check if column contains numeric values
                        try:
                            # Try to convert first non-empty value to float
                            first_value = next((v for v in values if v is not None and str(v).strip()), None)
                            if first_value:
                                float(str(first_value).replace(',', ''))
                                numeric_column = col
                        except (ValueError, TypeError):
                            # If conversion fails, it's probably a text column
                            if not text_column and any(isinstance(v, str) for v in values):
                                text_column = col
                    
                    if text_column and numeric_column:
                        # Create a simplified version for the graph
                        graph_data = {
                            text_column: result_data[text_column],
                            numeric_column: result_data[numeric_column]
                        }
                        return {
                            "content": response.get("output", ""),
                            "query_result": result_data,  # Keep full data for table
                            "graph_data": graph_data,     # Add simplified data for graph
                            "x_axis": text_column,
                            "y_axis": numeric_column
                        }
                
                return {
                    "content": response.get("output", ""),
                    "query_result": result_data
                }
        except Exception as e:
            error_msg = str(e)
            error_type = "syntax error" if "syntax error" in error_msg.lower() else "processing error"
            return {
                "content": "I apologize, but I encountered an error while processing your request. Please try rephrasing your question.",
                "query_result": {"error": f"There was an {error_type}.", "details": error_msg},
                "x_axis": [],
                "y_axis": [],
                "chartTitle": "Error in Query"
            }

    async def batch_query_nlp(self, queries: List[str], chat_id: str = None) -> List[Dict[str, Any]]:
        tasks = [self._process_single_query(query, chat_id) for query in queries]
        return await asyncio.gather(*tasks)

    def query_nlp(self, query: str, chat_id: str = None) -> Dict[str, Any]:
        return asyncio.run(self._process_single_query(query, chat_id))

    def query_nlp_text_only(self, prompt: str) -> str:
        return self.agent_executor.invoke({"input": prompt}).get("output", "")
