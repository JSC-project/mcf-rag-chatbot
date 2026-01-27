from __future__ import annotations
import re
import json
import lancedb

from pydantic_ai import Agent
from .data_models import RagResponse
from .constants import VECTOR_DATABASE_PATH

vector_db = lancedb.connect(uri=str(VECTOR_DATABASE_PATH))


rag_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=1,
    system_prompt=("""
        You MUST use the provided tool to retrieve documents before answering.
        Answer ONLY using information from the retrieved documents.
        If you cannot find the answer, respond with: "Sorry, I don't know that".
        Keep the answer short and clear.
        Always include the source title and source url.
        """
    ),
    output_type=RagResponse,
)


def _normalize(text: str) -> str:
    text = text.lower()
    # behåll svenska bokstäver, siffror och mellanslag
    text = re.sub(r"[^a-z0-9åäö\s\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _tokens(text: str) -> set[str]:
    # filtrera bort väldigt korta ord
    return {t for t in _normalize(text).split() if len(t) >= 3}


@rag_agent.tool_plain
def retrieve_top_documents(query: str, k: int = 3) -> str:
    table = vector_db.open_table("mcf_content")
    
    results = table.search(query).limit(k).to_list()
    if not results:
        return "No relevant douments"
    
    parts: list[str] = []

    for i, r in enumerate(results, start=1):
        title = r["title"]
        url = r["url"]
        content= ["content"]

        content_snippet = content[:1500]

        parts.append(
            f"[SOURCE {i}]\n"
            f"SOURCE_TITLE: {title}\n"
            f"SOURCE_URL: {url}\n"
            f"SOURCE_CONTENT:\n{content_snippet}\n"
            )

    return "\n".join(parts)


if __name__ == "__main__":
    result = rag_agent.run_sync("Får man ta med husdjur i skyddsrum?")
    print(result.output.model_dump_json(indent=2, ensure_ascii=False))
