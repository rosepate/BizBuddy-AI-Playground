import os
from dotenv import load_dotenv

load_dotenv()
print("OpenAI Key:", os.getenv("OPENAI_API_KEY"))
print("Groq Key:", os.getenv("GROQ_API_KEY"))
