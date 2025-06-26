import streamlit as st
import pandas as pd
import os
import sys
from dotenv import load_dotenv

# Make root folder importable to access agent module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the load_agent function from your agent module
from agent.bizbuddy_agent import load_agent

# Load environment variables
load_dotenv()

# ✅ Define chatbot function to be reused from main_app.py
def chatbot_view(agent):
    st.title("💬 BizBuddy AI Chatbot")
    st.markdown("Ask any question about your supplement sales data.")
    
# Streamlit UI Setup
st.set_page_config(page_title="BizBuddy AI", page_icon="🧠")
st.title("💬 BizBuddy AI")
st.markdown("Ask any question about your supplement sales data.")

# Text input from user
query = st.text_input("What would you like to know?", placeholder="e.g. Top 3 products by revenue in 2021")

# Load the LangChain agent
agent = load_agent()

# Run agent on user query
if st.button("Submit") and query:
    with st.spinner("Thinking..."):
        try:
            response = agent.run(query)
            st.success("✅ Answer:")
            st.write(response)
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

