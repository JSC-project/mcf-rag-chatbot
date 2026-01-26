import requests 
from bs4 import BeautifulSoup
from .utils import clean_text
from .models import MCFHeading, MCFLink, MCFPage, ExtractHtml

# html extraction model 
class ExtractHtml:
    def soup(url: str):
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

# fetch all links
class MCFLinkScraper:
    # website base url
    BASE_URL = "https://www.mcf.se"
    
    def __init__(self, start_path: str): 
        clean_path = start_path.strip("/") 
        self.start_url = f"{self.BASE_URL}/{clean_path}/"
    
    def scrape_links(self) -> MCFLink:
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

        return MCFLink(links=link_map)

# data scraper
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
            MCFHeading(
                level=tag.name,
                text=clean_text(tag.get_text(strip=True))
            )
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

        # extract in order according to source format
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

# if __name__ == "__main__":
    
#     html = MCFPageScraper(url).soup.prettify()

#     for start in range(300000, 365000, 5000):
#         print(f"\n--- BLOCK {start}–{start+5000} ---\n")
#         print(html[start:start+5000])

# sources:
# https://pypi.org/project/beautifulsoup4/
# copilot
# https://github.com/AIgineerAB/scraping-nbi/blob/main/scraper.py




        

