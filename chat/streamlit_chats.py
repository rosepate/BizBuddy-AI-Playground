import streamlit as st
import io
import os
import sys
from fpdf import FPDF
import pandas as pd

def chatbot_view(agent):
    st.title("💬 BizBuddy AI Chatbot")
    st.markdown("Chat naturally with your business data.")

    # 🗑️ Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        # Reset the agent to clear memory
        if "agent" in st.session_state:
            del st.session_state.agent
        # Reload the agent to reset memory
        from agent.bizbuddy_agent import load_agent
        st.session_state.agent = load_agent()  # Reset memory
        st.rerun()

    # Initialize chat history in Streamlit session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display past messages as chat bubbles
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

    # Input box (chat-style)
    user_input = st.chat_input("Ask your question...")

    if user_input:
        # Show user's message
        st.session_state.chat_history.append(("user", user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        # Agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = agent.run(user_input)
                    st.markdown(response)
                    st.session_state.chat_history.append(("assistant", response))
                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")

