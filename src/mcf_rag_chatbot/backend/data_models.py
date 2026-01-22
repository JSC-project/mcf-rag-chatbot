from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv
import os

load_dotenv() #Read the .env file for API-KEY

embeddings_model = get_registry().get("gemini-text").create(name="models/text-embedding-004") #Initialize the Gemini embedding model registry

class MCFContent(LanceModel):
    # Data model for storing scraped MCF content in LanceDB.

    url: str = Field(description="Käll-URL för den skrapade sidan för citat")
    title: str = Field(description="Titel på sidan eller specifikt avsnitt")

    # The SourceField indicates which text should be sent to the embedding model
    content: str = embeddings_model.SourceField()
from pydantic import BaseModel, Field

class RagResponse(BaseModel):
    answer: str = Field(description="Short answer based on retrieved content.")
    source_url: str | None = Field(default=None, description="URL to the source used.")
