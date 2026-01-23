from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv() #Read the .env file for API-KEY

#Initialize the Gemini embedding model registry
embeddings_model = get_registry().get("gemini-text").create(name="models/text-embedding-004") 



class MCFContent(LanceModel):
    """
    Data model/blueprint for our Knowledge Base.
    It defines how MCF web data is structured and vectorized.
    """ 
    
    # Fields for tracing the information back to the source
    url: str = Field(description="Käll-URL för den skrapade sidan för citat")
    title: str = Field(description="Titel på sidan eller specifikt avsnitt")

    # The SourceField tells LanceDB: Translate THIS text into a vector 
    content: str = embeddings_model.SourceField()

    # The 'VectorField' stores the AI's numerical understanding of the content.
    # We use 768 dimensions (the fixed output size of Gemini 004).
    vector: Vector(768) = embeddings_model.VectorField() # type: ignore

    # Automatically timestamp every entry when it's created
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class RagResponse(BaseModel):
    answer: str = Field(description="Short answer based on retrieved content.")
    source_url: str | None = Field(default=None, description="URL to the source used.")
    
class Prompt(BaseModel):
    prompt: str
