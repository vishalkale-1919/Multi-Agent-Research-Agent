import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_llm():
    """
    Initialize and return the Groq LLM instance.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_key_here":
        raise ValueError("GROQ_API_KEY is not set correctly in the .env file.")

    llm = ChatGroq(
        api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.2, # Low temperature for more factual and consistent responses
        max_tokens=4000
    )
    return llm
