import os
from utils.env_loader import load_env_variables
from utils.file_manager import FileManager
from database.db_manager import DatabaseManager
from agent.agent_manager import AgentManager

def main():
    """Main function to execute the workflow."""
    # api_key = load_env_variables()
    
    csv_path = os.path.abspath("data/titanic.csv")
    db_path = os.path.abspath("data/db.sqlite")

    df = FileManager.load_csv(csv_path)
    db_manager = DatabaseManager(db_path)

    db_manager.add_dataframe_as_table(df, "titanic")

    # agent_manager = AgentManager(api_key, db_manager.get_connection())

    # query = "Who are the passengers that paid the highest fare?"
    # response = agent_manager.execute_query(query)

    # for key, value in response.items():
    #     print(f"{key}: {value}\n")

if __name__ == "__main__":
    main()
