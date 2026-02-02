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
        
        Answer ONLY using information form the retrived documents.
        DO NOT replace explanations with references.
        the answer must stand on its own without requiring the user to visit the source.
                   
        If retrieve_top_documents returns NO_RELEVANT_DOCUMENTS, reply exactly:
        "Jag kan tyvärr inte svara på denna frågan...".
                   
        Provide detailed, practical gudiance for private individuals in Sweden.
        Explain why recommendations are given when the documents allow it.
        If multiple documents are relevant, combine the information into one clear answer.
                   
        Structure the response clearly using paragraphs or bullet points when helpful.
        Avoid generic or high-level summaries if the documents conatin concrete details.
                   
       Always end the answer with:
        - Source title
        - Source URL 
        """
    ),
    output_type=RagResponse,
)


@rag_agent.tool_plain
def retrieve_top_documents(query: str, k: int = 6) -> str:
    table = vector_db.open_table(TABLE_NAME)
    
    results = table.search(query).limit(k).to_list()
    if not results:
        return "NO_RELEVANT_DOCUMENTS"
    
    parts: list[str] = []

    for i, r in enumerate(results, start=1):
        title = r["title"]
        url = r["url"]
        content= r["content"]

        content_snippet = content[:1000]

        parts.append(
            f"[SOURCE {i}]\n"
            f"SOURCE_TITLE: {title}\n"
            f"SOURCE_URL: {url}\n"
            f"SOURCE_CONTENT:\n{content_snippet}\n"
            )

    return "\n".join(parts)


if __name__ == "__main__":
    print(retrieve_top_documents("Får man ta med husdjur i skyddsrum?"))
