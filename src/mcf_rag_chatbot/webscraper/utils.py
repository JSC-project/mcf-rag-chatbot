from .constants import DATA_PATH
import re
import json

BASE_URL = "https://www.mcf.se"

def clean_text(text: str) -> str:

        text = text.replace("\u00ad", "")  # soft hyphen

        text = re.sub(r"[\u200b\u200c\u200d]", "", text)  # zero-width chars

        return text

def export_data(data: dict, url: str):
    DATA_PATH.mkdir(parents=True, exist_ok=True)

    safe_name = url.replace(BASE_URL, "").strip("/").replace("/", "_")
    
    filepath = DATA_PATH / f"{safe_name}.json"

    with filepath.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"saved: {filepath}")