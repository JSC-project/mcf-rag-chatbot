import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE_URL = "https://www.mcf.se"
START_URL = "https://www.mcf.se/sv/rad-till-privatpersoner/hemberedskap---preppa-for-en-vecka/"
PREFIX = "/sv/rad-till-privatpersoner/hemberedskap---preppa-for-en-vecka/"

def fetch(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

# stop parsing flags
STOP_HEADINGS = {
    "Dela sidan med andra",
    "Relaterade länkar",
    "Om oss",
    "Våra tjänster",
    "Myndigheten i sociala medier",
    "Kontakta oss",
    "Webbplatsen",
}

SKIP_PATTERNS = [
    "Senast granskad",
    "Dela sidan på",
    "Kopiera sidans länk",
]

def should_skip(text: str) -> bool:
    return any(pat in text for pat in SKIP_PATTERNS)

def parse_page(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    main = soup.find("main") or soup

    # H1
    title_tag = main.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else ""

    headings = []
    for tag in main.find_all(["h2", "h3"]):
        text = tag.get_text(strip=True)
        headings.append({"level": tag.name, "text": text})

    parts = []
    stop = False

    # loop through page elements
    for el in main.descendants:
        if el.name in ["h2", "h3"]:
            h_text = el.get_text(strip=True)
            if h_text in STOP_HEADINGS:
                stop = True
                break

        if el.name == "p":
            text = el.get_text(strip=True)
            if text and not should_skip(text):
                parts.append(text)

        if el.name == "li":
            text = el.get_text(strip=True)
            if text and not should_skip(text):
                parts.append(f"- {text}")

    content = "\n".join(parts)

    return {
        "title": title,
        "headings": headings,
        "content": content,
    }

def extract_links(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(BASE_URL, href)
        parsed = urlparse(full_url)

        # prefix links only
        if parsed.path.startswith(PREFIX):
            links.append(full_url)

    return links

def save_page(data: dict, url: str):
    data_folder = Path(__file__).parent / "data" 
    data_folder.mkdir(exist_ok=True)

    safe_name = url.replace(BASE_URL, "").strip("/").replace("/", "_")
    filepath = data_folder / f"{safe_name}.json"

    with filepath.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"saved: {filepath}")

def crawl():
    to_visit = {START_URL}
    visited = set()

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue

        print(f"fetching: {url}")
        html = fetch(url)

        # extract and save
        page_data = parse_page(html)
        page_data["url"] = url
        save_page(page_data, url)

        # search for more links
        for link in extract_links(html):
            if link not in visited:
                to_visit.add(link)

        visited.add(url)

if __name__ == "__main__":
    crawl()

# sources:
# https://pypi.org/project/beautifulsoup4/
# copilot