from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.memory import ConversationBufferMemory
import pandas as pd
import os
from dotenv import load_dotenv

def load_agent():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = api_key

    # Load from Google Sheet CSV

    sheet_url = "https://docs.google.com/spreadsheets/d/1wKl1K0d0M_S_GUnOfw-duIhBc59YSU8KBKwWsPO26jI/export?format=csv"
    df = pd.read_csv(sheet_url)

# 🛡️ Handle date column gracefully
    if "Order Date" in df.columns:
        df.rename(columns={"Order Date": "Date"}, inplace=True)

    if "Date" in df.columns:
        try:
            df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
        except Exception as e:
            print("⚠️ Date conversion error:", e)

    # ✅ Check for important columns needed for analytics
    required_cols = ["Units Sold", "Revenue", "Cost Price", "Unit Price", "Profit", "Product", "Location", "Inventory After", "Date"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"⚠️ Missing key columns: {missing_cols}")

    # 🧾 Show columns and preview data
    print("🧾 Columns in dataset:", df.columns.tolist())
    print("🔍 Sample rows:\n", df.head())
    # ✅ Ensure all required columns are present
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    # ✅ Print first few rows for debugging
    print("🔍 Sample data:\n", df.head()
        )
    
    # ✅ Print column list for debugging
    print("🧾 Columns in dataset:", df.columns.tolist())

    # Set up the agent
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

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
    response = agent.invoke("What are the top 3 selling products by total number of sale?")
    print(response)
