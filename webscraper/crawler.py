import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup

URL = "https://www.mcf.se/sv/rad-till-privatpersoner/hemberedskap---preppa-for-en-vecka/"

def fetch_page(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else ""

    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    content = "\n".join(paragraphs)

    return {
        "title": title,
        "content": content
    }

def save_data(data, filename="page.json"):
    data_folder = Path(__file__).resolve().parent.parent / "data"
    
    data_folder.mkdir(exist_ok=True)

    filepath = data_folder / filename

    with filepath.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Saved to: {filepath}")

if __name__ == "__main__":
    html = fetch_page(URL)
    page_data = extract_text(html)
    page_data["url"] = URL

    save_data(page_data, "hemberedskap.json")



# sources:
# https://pypi.org/project/beautifulsoup4/
# copilot