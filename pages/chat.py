import streamlit as st
from utils.db import load_bots
from utils.graph import get_graph


bots = load_bots()
bot_names = [b['name'] for b in bots]

selected_name = ''
bot_id = ''
if bots:
    selected_name = st.sidebar.selectbox("Select Bot", bot_names)
    bot = next(b for b in bots if b['name'] == selected_name)
    bot_id = bot["bot_id"]

if selected_name == '' and bot_id == '':
    st.title("No Bots Available")
else:
    st.title(f"Chat with {selected_name}")

graph = get_graph()

if "messages" not in st.session_state:
    st.session_state.messages = {}

if bot_id not in st.session_state.messages:
    st.session_state.messages[bot_id] = []
if bots:
    if st.sidebar.button(f"Clear Chat History of {selected_name}"):
        st.session_state.messages[bot_id] = []
        st.rerun()

# Display history
for msg in st.session_state.messages[bot_id]:
    st.chat_message(msg["role"]).write(msg["content"])
if selected_name != '' and bot_id != '':
    query = st.chat_input("Ask something.....")
else:
    query = ''

if query:
    error = False
    if not st.session_state['PINECONE_API_KEY']:
        st.error("Plese enter Pinecone API Key")
        error = True
    if not st.session_state['OPENAI_API_KEY']:
        st.error("Plese enter Openai API key")
        error = True

    if not error:
        st.chat_message("user").write(query)
        
        response = graph.invoke({
            "query": query,
            "bot_id": bot_id,
            "context": [],
            "complete_context": [],
            "partial_context": [],
            "answer": "",
            "rag_needed": False,
            "zero_related": False,
            "answer_related": False,
            "max_tries": 0
        })

        st.chat_message("assistant").write(response['answer'])

        st.session_state.messages[bot_id].append({"role":"user", "content":query})
        st.session_state.messages[bot_id].append({"role":"assistant","content":response["answer"]})
    else:
        st.error("Please enter required api keys to proceed.")