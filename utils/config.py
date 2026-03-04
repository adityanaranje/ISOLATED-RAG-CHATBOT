import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()
from langchain_openai import ChatOpenAI

def get_api_key(key_name):
    # 1. Check session (user input)
    if key_name in st.session_state and st.session_state[key_name]:
        return st.session_state[key_name]

    # 2. Fallback to environment
    return 'None'

OPENAI_API_KEY = get_api_key("OPENAI_API_KEY")


llm = ChatOpenAI(
        model = "gpt-4o-mini",
        temperature = 0, 
        api_key = st.session_state['OPENAI_API_KEY']
    )

