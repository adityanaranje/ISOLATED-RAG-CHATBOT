import streamlit as st
from utils.db import load_bots
from utils.index import delete_bot_index

st.title("Manage Bots")

bots = load_bots()

if st.session_state['PINECONE_API_KEY'] and st.session_state['OPENAI_API_KEY']:
    if not bots:
        st.write("No Bots Available")

    for bot in bots:
        st.subheader(bot['name'])

        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"Delete {bot['name']}"):
                delete_bot_index(bot['bot_id'])
                st.success("Deleted")
                st.rerun()
        with col2:
            if st.button(f"Re-index {bot['name']}"):
                st.success("Re-indexed")
else:
    st.write("No API key Provided")