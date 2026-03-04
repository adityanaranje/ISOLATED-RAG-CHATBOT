from pinecone import Pinecone, ServerlessSpec
from utils.db import delete_bot
import streamlit as st


index_name = "rag-app"

def create_index():
    if st.session_state['PINECONE_API_KEY']:
        pc = Pinecone(api_key=st.session_state['PINECONE_API_KEY'])
        if index_name not in [i.name for i in pc.list_indexes()]:
            pc.create_index(
                name=index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
    else:
        st.error("PINECONE API Key Not provided.")


def delete_bot_index(bot_id):
    if st.session_state['PINECONE_API_KEY']:
        pc = Pinecone(api_key=st.session_state['PINECONE_API_KEY'])

        index = pc.Index(index_name)

        index.delete(
            delete_all=True,
            namespace=bot_id
        )

        delete_bot(bot_id)
    else:
        st.error("PINECONE API Key Not provided.")