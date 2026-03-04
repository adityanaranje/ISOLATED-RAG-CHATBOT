import streamlit as st
from utils.db import load_bots
from utils.index import create_index

st.set_page_config(page_title="RAG Bot Studio")

st.title("RAG Bot Studio")

if st.session_state['PINECONE_API_KEY'] and st.session_state['OPENAI_API_KEY']:
    st.subheader("Your Bots")

    bots = load_bots()

    if not bots:
        st.write("No Bots Created")
        create_index()


    for bot in bots:
        st.write(f"🧠 {bot['name']}")

    st.divider()

    if st.button("➕ Create New Bot"):
        st.switch_page("pages/create_bot.py")
else:
    st.write("No API key Provided.")

