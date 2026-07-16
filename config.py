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

def get_api_key() -> str:
    return get_secret("API_KEY")

def get_model_name() -> str:
    return get_secret("MODEL_NAME") or "mistral-small-2506"


API_KEY = None    
MODEL_NAME = None  