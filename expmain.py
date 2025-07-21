# main.py
import streamlit as st
import pandas as pd
import os
import sys
from dotenv import load_dotenv

# Initial setup
st.set_page_config(page_title="BizBuddy AI", page_icon="🧠", layout="wide")
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Load agent
from agent.agent import load_agent
agent = load_agent()

# Load dataset from Google Sheet
@st.cache_data(ttl=60)
def load_data():
      sheet_url = "https://docs.google.com/spreadsheets/d/1ISS7IQOMPrAEqU7lnpJYM5W2zd4oynntnmMTiokiVNU/export?format=csv"
      df = pd.read_csv(sheet_url)
      
      # Define column mapping based on potential Google Sheet names
      column_mapping = {
             "Sale Date": "Date",
             "Product Name": "Product",
             "Stock Level": "Inventory After",
             "Store": "Location"
         }
      required_cols = ["Date", "Product", "Inventory After", "Location", "Revenue", "Units Sold", "Unit Price", "Cost Price", "Profit", "Category", "Transaction ID", "Payment Method", "Platform"]
         
      # Rename columns if they exist
      df = df.rename(columns=column_mapping, errors="ignore")
         
      # Validate required columns
      missing_cols = [col for col in required_cols if col not in df.columns]
      if missing_cols:
             st.error(f"Missing required columns in dataset: {', '.join(missing_cols)}. Falling back to synthetic data.")
             df = pd.read_csv("synthetic_sales_data.csv")  # Fallback to synthetic data
             if "Sale Date" in df.columns:
                 df.rename(columns={"Sale Date": "Date"}, inplace=True)
         
      # Ensure Date is datetime
      df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
      
      return df

df = load_data()

# Import views
from chat.streamlit_chats import chatbot_view
from dashboard.streamlit_dashboards import dashboard_view

# Streamlit UI Setup
st.title("BizBuddy AI")
st.markdown("Welcome to BizBuddy AI! Use the navigation menu to explore the chatbot or dashboard.")

# Navigation
st.sidebar.title("🧽 Navigation")
page = st.sidebar.radio("Go to:", ["💬 Chatbot", "📊 Dashboard"])

# View rendering
if page == "💬 Chatbot":
    chatbot_view(agent)
elif page == "📊 Dashboard":
    dashboard_view(df)