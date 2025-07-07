import os
import streamlit as st
import requests

# API_URL = "https://adex-chatbot-api.onrender.com/chat"
API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="Document Chatbot")
st.title("📄 Static Document Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_chat_history():
    return [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]

# Display previous chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

query = st.chat_input("Ask something about the documents...")
if query:
    st.chat_message("user").write(query)
    st.session_state.messages.append({"role": "user", "content": query})

    try:
        response = requests.post(API_URL, json={
            "input": query,
            "history": get_chat_history()
        })
        response.raise_for_status()
        answer = response.json()["answer"]
    except Exception as e:
        answer = f"⚠️ Error: {e}"

    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})