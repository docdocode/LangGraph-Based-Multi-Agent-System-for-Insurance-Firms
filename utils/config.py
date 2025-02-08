from langchain.chat_models import ChatOpenAI  # Import ChatOpenAI instead of OpenAI
import os

def get_llm():
    """
    Returns an instance of the ChatOpenAI LLM with the model specified in the environment variable.
    Defaults to 'gpt-3.5-turbo' if no model is specified.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
    
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")  # Default to gpt-3.5-turbo
    return ChatOpenAI(api_key=api_key, model_name=model_name)