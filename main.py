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

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])


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
    
    except RateLimitError:
        st.warning("⚠️ Quota exhausted")
    
    st.markdown(answer)

