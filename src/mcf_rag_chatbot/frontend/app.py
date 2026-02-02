import streamlit as st
import base64
from pathlib import Path
from mcf_rag_chatbot.backend.rag import rag_agent
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ------------------------
# Background helper
# ------------------------
def get_base64_image(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ------------------------
# Paths
# ------------------------
current_dir = Path(__file__).parent
image_path = current_dir / "assets" / "4de476ee-1e0f-40c6-aa3f-7958bae6d9ae.webp"
css_path = current_dir / "style.css"

# ------------------------
# Session state
# ------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "page" not in st.session_state:
    st.session_state.page = "chat"

# ------------------------
# Load CSS
# ------------------------
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ------------------------
# Background
# ------------------------
img_base64 = get_base64_image(image_path)

st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(rgba(0, 31, 63, 0.82), rgba(0, 31, 63, 0.82)), 
    url("data:image/webp;base64,{img_base64}") no-repeat center center fixed;
    background-size: cover;
}}
</style>
""", unsafe_allow_html=True)

# ------------------------
# Sidebar navigation
# ------------------------
st.sidebar.markdown("### Navigation")

if st.sidebar.button("💬 Chatbot"):
    st.session_state.page = "chat"

if st.sidebar.button("🛡️ Skyddsrum"):
    st.session_state.page = "shelter"

# ========================
# CHAT PAGE
# ========================
if st.session_state.page == "chat":

    st.title("MCF-Chatbot 🤖")
    st.write("Välkommen till MCF-Chatbot! Här kan du ställa frågor som berör beredskap vid kris eller krig")

    # Show history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ställ din fråga...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Söker svar..."):
                try:
                    result = rag_agent.run_sync(prompt)

                    ans = result.output.answer
                    res_url = result.output.url
                    res_title = result.output.title

                    if res_url:
                        full_response = f"{ans}\n\n**Källa:** [{res_title}]({res_url})"
                    else:
                        full_response = ans

                    st.markdown(full_response)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": full_response}
                    )

                except Exception as e:
                    st.error(f"Ett fel uppstod: {e}")

# ========================
# SKYDDSRUM PAGE
# ========================
else:

    st.title("Skyddsrum 🛡️")
    st.write("Här kan ni senare lägga in skyddsrumssökning eller karta.")
