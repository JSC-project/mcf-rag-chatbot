import base64
from pathlib import Path
import streamlit as st

def _b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()

def apply_ui(bg_filename: str):
    root = Path(__file__).parent  # .../frontend
    css_path = root / "style.css"
    img_path = root / "assets" / bg_filename

    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

    if img_path.exists():
        img64 = _b64(img_path)
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: linear-gradient(rgba(0, 31, 63, 0.82), rgba(0, 31, 63, 0.82)),
                url("data:image/webp;base64,{img64}") no-repeat center center fixed;
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
