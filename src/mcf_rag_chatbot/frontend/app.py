import streamlit as st
import base64
from pathlib import Path
from mcf_rag_chatbot.backend.rag import rag_agent #revice the rag agent

# Function for background image
def get_base64_image(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
# Paths
current_dir = Path(__file__).parent
root_path = Path(__file__).parents[3]
image_path = root_path / "assets" / "4de476ee-1e0f-40c6-aa3f-7958bae6d9ae.webp"
css_path = current_dir / "style.css"

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Background Image Processing
img_base64 = get_base64_image(image_path)

# Apply CSS from style.css
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Set Dynamic Background (Base64)
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 31, 63, 0.82), rgba(0, 31, 63, 0.82)), 
        url("data:image/webp;base64,{img_base64}") no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- UI ---
st.title("MCF-Chatbot 🤖")
st.write("Välkommen till MCF-Chatbot! Här kan du ställa frågor som berör beredskap vid kris eller krig")

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input and RAG Integration
if prompt := st.chat_input("Ställ din fråga..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate answer from RAG
    with st.chat_message("assistant"):
        with st.spinner("Söker svar..."):
            try:
                # Run Agent
                result = rag_agent.run_sync(prompt)
                
                # Recive text from pydantic-modell (RagResponse)
                ans = result.output.answer
                res_url = result.output.url
                res_title = result.output.title
                
                

                #Display response
                if res_url:
                    full_response = f"{ans}\n\n**Källa:** [{res_title}]({res_url})"
                else:
                    full_response = ans
                
                
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                
            except Exception as e:
            # Ta bort IF-satsen för DOCS_PATH eftersom den variabeln är död nu
                st.error(f"Ett fel uppstod: {e}")
                
