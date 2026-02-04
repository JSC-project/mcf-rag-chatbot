import streamlit as st
import base64
from pathlib import Path
import os
import requests
from src.mcf_rag_chatbot.backend.faq import FAQHandler

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def get_base64_image(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Paths (OBS: vi är i pages/, så vi går upp ett steg till frontend/)
current_dir = Path(__file__).parent.parent
image_path = current_dir / "assets" / "4de476ee-1e0f-40c6-aa3f-7958bae6d9ae.webp"
css_path = current_dir / "style.css"

# FAQ handler init
project_root = Path(__file__).parents[2]  # mcf_rag_chatbot/
faq_log_path = project_root / "data" / "faq" / "questions.json"
faq_handler = FAQHandler(faq_log_path)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Background Image Processing
img_base64 = get_base64_image(image_path)

# Apply CSS from style.css
with open(css_path, encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Set Dynamic Background (Base64)
st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 31, 63, 0.82), rgba(0, 31, 63, 0.82)), 
        url("data:image/webp;base64,{img_base64}") no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- UI ---
st.title("MCF-Chatbot 🤖")
st.write("Välkommen till MCF-Chatbot! Här kan du ställa frågor som berör beredskap vid kris eller krig")

# FAQ-sektion
st.subheader("💡 Vanliga frågor")

top_questions = faq_handler.get_top_questions()
cols = st.columns(2)
clicked_question = None

for i, question in enumerate(top_questions):
    if cols[i % 2].button(question):
        clicked_question = question




# Display Messages (historik)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✅ Chat input (ska ligga här)
prompt = st.chat_input("Ställ din fråga...")

try:
    resp = requests.post(
        f"{API_URL.rstrip('/')}/rag/query",
        json={"prompt": prompt},
        timeout=90,
    )

    if resp.status_code == 503:
        st.warning("LLM är överbelastad just nu. Försök igen om en liten stund.")
        st.stop()

    resp.raise_for_status()
    data = resp.json()

    # data är RagResponse som JSON
    ans = data.get("answer", "")

    # Om RagResponse har url/title så används de, annars visar vi bara ans
    res_url = data.get("url", "") or data.get("source_url", "")
    res_title = data.get("title", "") or "Källa"

    if res_url:
        full_response = f"{ans}\n\n**Källa:** [{res_title}]({res_url})"
    else:
        full_response = ans

    st.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

except requests.exceptions.RequestException as e:
    st.error(f"Kunde inte nå backend API: {e}")

