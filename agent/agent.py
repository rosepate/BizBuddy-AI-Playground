from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.memory import ConversationBufferMemory
import pandas as pd
import os
from dotenv import load_dotenv

def load_agent():
    # Load environment
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = api_key

    # Load dataset
    df = pd.read_csv("agent/Supplement_Sales_Weekly_Expanded.csv")

    # Set up LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # ✅ Add memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Create agent with memory
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        memory=memory,
        handle_parsing_errors=True,
        agent_type="openai-tools",
        allow_dangerous_code=True,
    )

    return agent
if __name__ == "__main__":
    agent = load_agent()
    # Test the agent with a sample query
    response = agent.run("What are the top 3 selling products by total number of sale?")
    print(response)
