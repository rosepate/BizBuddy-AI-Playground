import os
import pandas as pd
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# Load environment variables from .env file
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ✅ Force it into global environment for LangChain
os.environ["OPENAI_API_KEY"] = api_key


from langchain_community.chat_models import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)