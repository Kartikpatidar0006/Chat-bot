import os
from dotenv import load_dotenv

load_dotenv()

def get_secret(key: str) -> str:
    """
    Local pe: .env file se padhta hai
    Streamlit Cloud pe: st.secrets se padhta hai
    """
    try:
        import streamlit as st
        return st.secrets.get(key) or os.getenv(key, "")
    except Exception:
        return os.getenv(key, "")

API_KEY = get_secret("API_KEY")
MODEL_NAME = get_secret("MODEL_NAME")