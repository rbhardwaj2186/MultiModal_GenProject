import requests
import streamlit as st

st.title("FastAPI Image Generator ChatBot")

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.image(message["content"])


if prompt := st.chat_input("Write your prompt in this input field"):


    with st.chat_message("assistant"):
        response = requests.get(
            f"http://localhost:8000/generate/image?prompt={prompt}"
        ).content
        st.text("Here is your generated image")
        st.image(response)

