import streamlit as st

def chatbot_view(agent):
    st.title("💬 BizBuddy AI Chatbot")
    st.markdown("Ask any question about your supplement sales data.")

    query = st.text_input("What would you like to know?", placeholder="e.g. Top 3 products by revenue in 2021")

    if st.button("Submit") and query:
        with st.spinner("Thinking..."):
            try:
                response = agent.run(query)
                st.success("✅ Answer:")
                st.write(response)
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")
