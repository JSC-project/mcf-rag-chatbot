from pydantic import BaseModel, Field 
import requests 
from bs4 import BeautifulSoup
from typing import List, Dict

# scraper models
class MCFHeading(BaseModel):
    level: str 
    text: str
    
class MCFPage(BaseModel): 
    url: str 
    title: str 
    headings: List[MCFHeading] 
    content: str

class MCFLink(BaseModel): 
    links: Dict[str, str] = Field( 
        description="Dict with slug → full URL" )

# html extraction model 
class ExtractHtml:
    def soup(url: str):
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")