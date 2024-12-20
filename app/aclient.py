import requests
import streamlit as st

st.title("FastAPI Audio ChatBot")

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        if isinstance(content, bytes):
            st.audio(content)
        else:
            st.markdown(content)

if prompt := st.chat_input("Write your prompt in this input field"):
    with st.chat_message("assistant"):
        response = requests.get(
            f"http://localhost:8000/generate/audio?prompt={prompt}"
        ).content
        st.text("Here is your generated audio")
        st.audio(response)