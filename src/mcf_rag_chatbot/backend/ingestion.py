import json
from .database import ingest_raw_content
from .constants import DATA_PATH

def run():
    print(f"Letar efter JSON-filer i: {DATA_PATH}")

    #Finds the files the crawler created
    files = list(DATA_PATH.glob("*.json"))

    if not files:
        print("Hittade inga filer! Kör crawlern först.")
        return

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"Embeddar: {data.get('title')}")
            
            
            ingest_raw_content(
                url=data.get("url"),
                title=data.get("title"),
                raw_text=data.get("content")
            )

if __name__ == "__main__":
    run()