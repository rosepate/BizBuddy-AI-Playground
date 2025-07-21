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

# Load dataset
@st.cache_data(ttl=60)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1ktXvN1Y7HTVkM0WQhuEV8nyk8_NfWSi_7v2rSphbaN4/export?format=csv"
    df = pd.read_csv(sheet_url)
    # Rename Sale Date to Date if it exists
    if "Sale Date" in df.columns:
        df.rename(columns={"Sale Date": "Date"}, inplace=True)
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
