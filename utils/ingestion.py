from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
import streamlit as st

embeddings = OpenAIEmbeddings(api_key=st.session_state['OPENAI_API_KEY'])

def ingest_doc(files, bot_id):
    docs = []

    for file in files:
        with open(f"Docs/temp_{file.name}", "wb") as f:
            f.write(file.getbuffer())
        
        loader = PyPDFLoader(f"Docs/temp_{file.name}")
        docs.extend(loader.load())
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500, 
        chunk_overlap = 200
        )
    chunks = splitter.split_documents(docs)

    for chunk in chunks:
        chunk.metadata["bot_id"] = bot_id

    PineconeVectorStore.from_documents(
        documents = chunks,
        embedding = embeddings,
        index_name = "rag-app",
        namespace=bot_id,
        pinecone_api_key=st.session_state["PINECONE_API_KEY"]
    )