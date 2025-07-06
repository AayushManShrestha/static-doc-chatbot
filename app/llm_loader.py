# app/llm_loader.py
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import GOOGLE_API_KEY, LLM_MODEL

def load_llm():
    return ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3
    )
