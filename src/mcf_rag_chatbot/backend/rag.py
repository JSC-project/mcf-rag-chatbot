from __future__ import annotations
import lancedb
from pydantic_ai import Agent
from .data_models import RagResponse
from .constants import VECTOR_DATABASE_PATH, TABLE_NAME

vector_db = lancedb.connect(uri=str(VECTOR_DATABASE_PATH))


rag_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=1,
    system_prompt=("""
        You MUST use the provided tool to retrieve documents before answering.
        Answer ONLY using information from the retrieved documents.
        If retrieve_top_documents returns NO_RELEVANT_DOCUMENTS, reply exactly: "Sorry, I don't know that".
        Keep the answer short and clear.
        Always include the source title and source url.
        """
    ),
    output_type=RagResponse,
)


@rag_agent.tool_plain
def retrieve_top_documents(query: str, k: int = 3) -> str:
    table = vector_db.open_table(TABLE_NAME)
    
    results = table.search(query).limit(k).to_list()
    if not results:
        return "NO_RELEVANT_DOCUMENTS"
    
    parts: list[str] = []

    for i, r in enumerate(results, start=1):
        title = r["title"]
        url = r["url"]
        content= r["content"]

        content_snippet = content[:1500]

        parts.append(
            f"[SOURCE {i}]\n"
            f"SOURCE_TITLE: {title}\n"
            f"SOURCE_URL: {url}\n"
            f"SOURCE_CONTENT:\n{content_snippet}\n"
            )

    return "\n".join(parts)


if __name__ == "__main__":
    print(retrieve_top_documents("Får man ta med husdjur i skyddsrum?"))
