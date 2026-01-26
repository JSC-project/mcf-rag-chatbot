from pathlib import Path 
import requests 
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field 
from typing import List, Dict
from mcf_rag_chatbot.backend.constants import DATA_PATH

# models
class MCFHeading(BaseModel):
    level: str # html headings
    text: str
    
class MCFPage(BaseModel): 
    url: str 
    title: str 
    headings: List[MCFHeading] 
    content: str

class MCFLinkMap(BaseModel): 
    links: Dict[str, str] = Field( 
        description="Dict with slug → full URL" )

# html extraction model 
class ExtractHtml:
    
    def soup(url: str):
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

# fetch all artickle links
class MCFLinkScraper:
    
    # website base url
    BASE_URL = "https://www.mcf.se"
    
    def __init__(self, start_path: str): 
        clean_path = start_path.strip("/") 
        self.start_url = f"{self.BASE_URL}/{clean_path}/"
    
    def scrape_links(self) -> MCFLinkMap:
        soup = ExtractHtml.soup(self.start_url)

        links = soup.select("a[href]")
        article_links = set()

        for a in links:
            href = a["href"]

            # internal site links only
            if href.startswith("/"):
                full = self.BASE_URL + href
            elif href.startswith(self.BASE_URL):
                full = href
            else:
                continue

            # only links in same section
            if full.startswith(self.start_url):
                article_links.add(full)

        # slug → url
        link_map = {url.rstrip("/").split("/")[-1]: url for url in article_links}

        return MCFLinkMap(links=link_map)

# page scraper
class MCFPageScraper:
    def __init__(self, url: str):
        self.url = url
        self.soup = ExtractHtml.soup(url)

    def _find_article_container(self):
        soup = self.soup

        # try finding via <main id="app">
        main = soup.find("main", id="app")
        if main:
            # välj column-content med h1 om möjligt
            candidates = main.find_all("div", class_="column-content")
            for c in candidates:
                if c.find("h1"):
                    return c

        # all column-content, välj den som har h1
        candidates = soup.find_all("div", class_="column-content")
        for c in candidates:
            if c.find("h1"):
                return c

        # fallbacks
        alt = soup.find("div", class_="page-content")
        if alt:
            return alt

        alt2 = soup.find("div", class_="content-area")
        if alt2:
            return alt2

        return soup.find("main") or soup

            
    def extract(self) -> MCFPage:
        article = self._find_article_container()

        # title
        h1 = article.find("h1")
        title = h1.get_text(strip=True) if h1 else ""

        # headings
        headings = [
            MCFHeading(level=tag.name, text=tag.get_text(strip=True))
            for tag in article.find_all(["h2", "h3"])
        ]

        # find intro + main body
        intro = article.find("div", class_="page-intro")
        body = article.find("div", class_="page-main-body") or article

        # combine containers in order
        containers = []
        if intro:
            containers.append(intro)
        containers.append(body)

        parts = []

        # extract in correct DOM order
        for container in containers:
            for element in container.descendants:
                if element.name == "p":
                    text = element.get_text(strip=True)
                    if text:
                        parts.append(text)

                elif element.name == "li":
                    text = element.get_text(strip=True)
                    if text:
                        parts.append(f"- {text}")

        content = "\n".join(parts)

        return MCFPage(
            url=self.url,
            title=title,
            headings=headings,
            content=content,
        )

    def save_page(data: dict, url: str):
        DATA_PATH.mkdir(parents=True, exist_ok=True)

        safe_name = url.replace(BASE_URL, "").strip("/").replace("/", "_")
        filepath = DATA_PATH / f"{safe_name}.json"

        with filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"saved: {filepath}")

if __name__ == "__main__":

    print("Hämtar länkar...\n")

    links = MCFLinkScraper(
        "sv/rad-till-privatpersoner/hemberedskap---preppa-for-en-vecka"
    ).scrape_links()

    print(f"Hittade {len(links.links)} länkar:")
    for slug, url in links.links.items():
        print(f" - {slug} → {url}")

    print("\nTestar första sidan...\n")

    # välj en specifik sida för att vara säker
    test_slug = "beredskap-for-dina-husdjur"
    url = links.links.get(test_slug) or next(iter(links.links.values()))

    page = MCFPageScraper(url).extract()
    print(page.model_dump())
        
    #html = MCFPageScraper(url).soup.prettify() # checking html structure







        

