from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import streamlit as st

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key = st.session_state['OPENAI_API_KEY'])

def get_retriever(bot_id):
    vectorstore = PineconeVectorStore(
        index_name = "rag-app",
        embedding = embeddings,
        namespace = bot_id
    )

    return vectorstore.as_retriever(search_kwargs = {"k":5})
