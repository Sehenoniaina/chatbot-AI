import os
import streamlit as st
from openai import OpenAI, RateLimitError
from groq import Groq
from dotenv import load_dotenv
import time


load_dotenv()

# Récupération du clé API
GROQ_KEY = os.getenv("GROQ_API_KEY")

# Initialisation du client
groq_client = Groq(api_key=GROQ_KEY)
st.markdown("Welcome in Chatbot AI")


if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

if "active_chat" not in st.session_state:
    st.session_state.active_chat = None

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

if st.sidebar.button(label="New chat"):
    st.session_state.messages = []
    st.session_state.active_chat = None
    st.rerun()

# side bar
with st.sidebar:
    st.header('Request history')
    st.markdown("""
    <style>
    div.stButton > button {
        background-color: transparent;
        border: none;
        width: 100%;
        text-align: left;
        padding: 8px 10px;
        border-radius: 5px;
        transition: background-color 0.2s;
    }
    div.stButton > button:hover {
        background-color: #c0c0c0;
    }
    div.stButton > button:active {
        background-color: #c0c0c0; 
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    for i, chat in enumerate(st.session_state.history):
        if st.button(chat["title"], key=f"history_{i}"):
            st.session_state.messages = chat['messages'].copy()
            st.session_state.active_sheet = i
            st.rerun()
    
prompt = st.chat_input("Write your message...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",  
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.choices[0].message.content
        st.session_state.messages.append({"role": "system", "content": answer})
        with st.spinner("Wait for it ....", show_time=False):
            time.sleep(1)
        st.success("✅ Answer ")
        st.markdown(answer)
        if st.session_state.active_chat is None:
            # if new chat , add in history
            st.session_state.history.append({
                "title": prompt[:30] + ("..." if len(prompt) > 30 else ""),
                "messages": st.session_state.messages.copy()
            })
            st.session_state.active_chat = len(st.session_state.history) - 1
        else:
            # if chat existed, update message
            st.session_state.history[st.session_state.active_chat]["messages"] = st.session_state.messages.copy()

    
    except RateLimitError:
        st.warning("⚠️ Quota exhausted")

