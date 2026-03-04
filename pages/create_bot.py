import streamlit as st
import uuid
from utils.db import save_bot
from utils.ingestion import ingest_doc



st.title("➕ Create New Bot")

if st.session_state['PINECONE_API_KEY'] and st.session_state['OPENAI_API_KEY']:
    name = st.text_input("Bot Name")
    files = st.file_uploader(
        "Upload Documents",
        accept_multiple_files=True,
        type=["pdf"]
    )

    if st.button("Create Bot"):
        if not name or not files:
            st.error("Provide name and documents")
        else:
            bot_id = str(uuid.uuid4())

            with st.spinner("Processing documents...."):
                ingest_doc(files, bot_id)
            save_bot({
                "bot_id":bot_id,
                "name":name,
                "files":[f.name for f in files]
            })
            
            st.success("Bot Created Successfully!")
            st.switch_page("pages/chat.py")
else:
    st.write("No API key Provided")
