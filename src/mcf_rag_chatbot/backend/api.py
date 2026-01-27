from fastapi import FastAPI, HTTPException
from pydantic_ai.exceptions import ModelHTTPError
from .data_models import Prompt
from .rag import rag_agent, vector_db

app = FastAPI()



@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# api query function
@app.post("/rag/query")
async def query_documentation(query: Prompt):
    try:
        result = await rag_agent.run(query.prompt)
        return result.output
    except ModelHTTPError as e:
        # om modellen är överbelastad
        if e.status_code == 503:
            raise HTTPException(status_code=503, detail="LLM overloaded. Try again.")
        raise HTTPException(status_code=502, detail=f"LLM error: {e.status_code}")


#LLM-generated for testingg to retrive data from lancedb
@app.get("/rag/retrieve")
def rag_retrieve(q: str, k: int = 3):
    try:
        table = vector_db.open_table("mcf_content")
        results = table.search(q).limit(k).to_list()
        return {
            "count": len(results),
            "results": [
                {
                    "title": r.get("title"),
                    "url": r.get("url"),
                    "distance": r.get("_distance"),
                    "content_preview": (r.get("content") or "")[:200],
                }
                for r in results
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))