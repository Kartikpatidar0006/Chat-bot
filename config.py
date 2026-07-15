import os
from dotenv import load_dotenv

load_dotenv()

def get_secret(key: str) -> str:
    """
    Runtime pe secrets padhta hai:
    - Streamlit Cloud: st.secrets se
    - Local: .env se
    """
    try:
        import streamlit as st
        val = st.secrets.get(key, "")
        if val:
            return str(val)
    except Exception:
        pass
    return os.getenv(key, "")

# These are called lazily — import time pe nahi
def get_api_key() -> str:
    return get_secret("API_KEY")

def get_model_name() -> str:
    return get_secret("MODEL_NAME") or "mistral-small-2506"

# Backward compatibility ke liye (kuch files directly import karte hain)
API_KEY = None    # llm.py ab get_api_key() call karega
MODEL_NAME = None  # llm.py ab get_model_name() call karega