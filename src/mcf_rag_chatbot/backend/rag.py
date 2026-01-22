from __future__ import annotations
from dotenv import load_dotenv
import re
import json
from pathlib import Path

from pydantic_ai import Agent
from .data_models import RagResponse

load_dotenv()


DOCS_PATH = Path("data/dev_docs.json")


rag_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=1,
    system_prompt=(
        "You are an expert in civil defence. "
        "Use the provided tool to retrieve relevant documents before answering. "
        "Do not make up any answers. "
        "If you can't find a good answer in the retrieved documents, respond with: \"Sorry, I don't know that\". "
        "Keep the answer short and clear. Do not give out more information than necessary. "
        "Always give a link to the source URL."
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
    
    print("retrieve_top_documents called with:", query)  # kan tas bort senare

    docs = json.loads(DOCS_PATH.read_text(encoding="utf-8"))
    if not isinstance(docs, list):
        return "NO_RELEVANT_DOCUMENTS"

    q_tokens = _tokens(query)
    if not q_tokens:
        return "NO_RELEVANT_DOCUMENTS"

    def score(doc: dict) -> int:
        content = doc.get("content", "")
        return len(q_tokens & _tokens(content))

    ranked = sorted(docs, key=score, reverse=True)
    ranked = [d for d in ranked if score(d) > 0]

    if not ranked:
        return "NO_RELEVANT_DOCUMENTS"

    top = ranked[:k]

    # Bygg en kontext som är lätt för modellen att använda + citera
    parts: list[str] = []
    for i, doc in enumerate(top, start=1):
        title = doc.get("title", "Untitled")
        url = doc.get("url", "")
        content = doc.get("content", "")

        # Begränsa storleken så prompten inte blir enorm
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
