import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from utils.config import LANGUAGE_MODEL, TEMPERATURE, MAX_NEW_TOKENS

load_dotenv()

def get_llm(model_name=LANGUAGE_MODEL):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in a .env file.")
    
    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        temperature=TEMPERATURE,
        max_tokens=MAX_NEW_TOKENS
    )
