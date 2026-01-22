from pydantic import BaseModel, Field

class RagResponse(BaseModel):
    answer: str = Field(description="Short answer based on retrieved content.")
    source_url: str | None = Field(default=None, description="URL to the source used.")
