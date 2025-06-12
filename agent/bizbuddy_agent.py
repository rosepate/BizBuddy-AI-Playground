
def load_agent():
    from langchain_openai import ChatOpenAI
    from langchain_experimental.agents import create_pandas_dataframe_agent
    import pandas as pd
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()

    # Load dataset
    df = pd.read_csv("Supplement_Sales_Weekly_Expanded.csv")
    # Display first few rows of the dataframe
    print(df.head())

    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")

    # Confirm key loaded (for debug only, remove later)
    print("API Key:", api_key)

    # ✅ Force it into global environment for LangChain
    os.environ["OPENAI_API_KEY"] = api_key
    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    )
    # Create the DataFrame agent
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        allow_dangerous_code=True  # ✅ this fixes the error
    )
    # Note: allow_dangerous_code=True is used here for demonstration purposes.

    return agent


    
if __name__ == "__main__":
    agent = load_agent()
    # Try a sample query
    response = agent.run("What are the top 3 selling products by total number of sale?")
    print(response)
