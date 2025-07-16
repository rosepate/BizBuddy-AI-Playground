from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.memory import ConversationBufferMemory
import pandas as pd
import os
from dotenv import load_dotenv
import streamlit as st

def load_agent():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    os.environ["OPENAI_API_KEY"] = api_key

    # Load from Google Sheet CSV
    sheet_url = "https://docs.google.com/spreadsheets/d/1wKl1K0d0M_S_GUnOfw-duIhBc59YSU8KBKwWsPO26jI/export?format=csv"
    
    try:
        df = pd.read_csv(sheet_url)
        print(f"✅ Successfully loaded data with shape: {df.shape}")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

    # 🧾 Show original columns for debugging
    print("🔍 Original columns:", df.columns.tolist())
    
    # Clean and normalize column names
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace("\uFEFF", "")  # Remove BOM
    df.columns = df.columns.str.strip('"')  # Remove quotes
    
    # 🧾 Show cleaned columns
    print("🧾 Cleaned columns:", df.columns.tolist())
    
    # Display in Streamlit sidebar if available
    if 'st' in globals():
        try:
            st.sidebar.write("🧾 Columns in sheet:", df.columns.tolist())
        except:
            pass  # Streamlit not available or sidebar not accessible

    # Rename common variations to standard names
    column_mappings = {
        "Product Name": "Product",
        "﻿Product": "Product",  # handles BOM character
        " Product": "Product",
        "Order Date": "Date",
        "Transaction ID": "Transaction_ID",
        "Customer ID": "Customer_ID",
        "Units Sold": "Units_Sold",
        "Unit Price": "Unit_Price",
        "Cost Price": "Cost_Price",
        "Inventory After": "Inventory_After",
        "Payment Method": "Payment_Method",
        "Expiry Date": "Expiry_Date",
        "Promo Active": "Promo_Active",
        "Discount (%)": "Discount_Percent"
    }
    
    for old_name, new_name in column_mappings.items():
        if old_name in df.columns:
            df.rename(columns={old_name: new_name}, inplace=True)
            print(f"✅ Renamed '{old_name}' to '{new_name}'")

    # 🛡️ Handle date column gracefully
    if "Date" in df.columns:
        try:
            df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
            print("✅ Date column converted successfully")
        except Exception as e:
            print(f"⚠️ Date conversion error: {e}")

    # ✅ Check for important columns needed for analytics
    required_cols = ["Units_Sold", "Revenue", "Cost_Price", "Unit_Price", "Profit", "Product", "Location", "Inventory_After", "Date"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        print(f"⚠️ Missing key columns: {missing_cols}")
        print(f"📋 Available columns: {df.columns.tolist()}")
        
        # Try to find similar columns
        for missing_col in missing_cols:
            similar_cols = [col for col in df.columns if missing_col.lower().replace('_', ' ') in col.lower() or col.lower().replace('_', ' ') in missing_col.lower()]
            if similar_cols:
                print(f"🔍 Possible matches for '{missing_col}': {similar_cols}")

    # 🧾 Show final columns and preview data
    print("🧾 Final columns in dataset:", df.columns.tolist())
    print("🔍 Sample rows:")
    print(df.head())
    
    # Check data types
    print("📊 Data types:")
    print(df.dtypes)
    
    # Check for null values
    print("🔍 Null values per column:")
    print(df.isnull().sum())

    # Set up the agent with proper error handling
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        
        # Create agent without deprecated parameters
        agent = create_pandas_dataframe_agent(
            llm,
            df,
            verbose=True,
            agent_type="openai-tools",
            allow_dangerous_code=True,
        )
        
        print("✅ Agent created successfully")
        return agent
        
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        return None

def test_agent(agent):
    """Test the agent with a simple query"""
    if agent is None:
        print("❌ Agent not available for testing")
        return None
    
    try:
        # Simple test query
        test_queries = [
            "What are the column names in this dataset?",
            "How many rows are in this dataset?",
            "What are the top 3 products by revenue?",
            "What are the top 3 selling products by total units sold?"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing query: {query}")
            try:
                response = agent.invoke(query)
                print(f"✅ Response: {response}")
            except Exception as e:
                print(f"❌ Error with query '{query}': {e}")
                continue
                
    except Exception as e:
        print(f"❌ Error testing agent: {e}")

if __name__ == "__main__":
    agent = load_agent()
    
    if agent:
        test_agent(agent)
    else:
        print("❌ Failed to load agent")