import streamlit as st
import asyncio
import requests
from pathlib import Path


# Configs
st.set_page_config(page_title="MCF-Chatbot", layout="centered")

#CSS
# CSS
st.markdown("""
    <style>
    /* Background */
    .stApp {
        background-color: #001f3f;
    }
    
    /* Force ALL text (titles, body text, labels) to be white */
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, h1, h2, h3, p {
        color: #ffffff !important;
    }

    /* Makes the title more pretty and clear  */
    h1 {
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        font-weight: 800;
    }

    
    .stChatInput textarea {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("MCF-Chatbot 🤖")
st.write("Välkommen till din AI assistent som hjälper dig besvara frågor gällande beredskap")


# Create the container for chathistory if not exist
if "message" not in st.session_state: 
    st.session_state.message = []

# Show all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat-input: Here the user ask their question
if prompt := st.chat_input("Ställ din fråga..."):
    # Saves and show the users question
    st.session_state.message.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


