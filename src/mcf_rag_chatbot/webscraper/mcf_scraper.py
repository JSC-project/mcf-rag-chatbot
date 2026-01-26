from pathlib import Path 
import requests 
from bs4 import BeautifulSoup

# extracting html and returns beautifulsoup 
class ExtractHtml:
    
    def soup(url: str):
        response = requests.get(url, timeout=10)
        response.reaise_for_status()
        return BeautifulSoup(response.text, "html.parser")

# 