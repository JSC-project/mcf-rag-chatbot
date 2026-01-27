from fastapi import FastAPI
from .data_models import Prompt
from .rag import rag_agent
app = FastAPI()

# root page message
@app.get("/")
def root():
    return {"Chatbot API is running. http://127.0.0.1:8000/docs for swagger UI"}

# api query function
@app.post("/rag/query")
async def query_documentation(query: Prompt):
    result = await rag_agent.run(query.prompt)
    return result.output