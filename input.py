import streamlit as st
import os
from langchain_openai import OpenAI
from pinecone import Pinecone
port = int(os.environ.get("PORT", 8501))

pinecone_api_key = st.text_input("Enter Pinecone API Key", type="password")
openai_api_key = st.text_input("Enter OpenAI API Key", type="password")




st.session_state['PINECONE_API_KEY'] = pinecone_api_key
st.session_state['OPENAI_API_KEY'] = openai_api_key

if st.button("Proceed"):
    try:
        pc = Pinecone(api_key=pinecone_api_key)
        pc.list_indexes()

        client = OpenAI(api_key=openai_api_key)
        os.environ["PINECONE_API_KEY"] = st.session_state.get("PINECONE_API_KEY")
        st.switch_page("pages/app.py")
    except Exception as e:
        st.session_state['PINECONE_API_KEY'] = ''
        st.session_state['OPENAI_API_KEY'] = ''
        st.error("Invalid API Key")
