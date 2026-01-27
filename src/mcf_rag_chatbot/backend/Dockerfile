FROM python:3.13-slim

# path inside of the container
WORKDIR /app

COPY knowledge_base knowledge_base
COPY src/mcf_rag_chatbot/backend backend
COPY pyproject.toml uv.lock ./
COPY src/mcf_rag_chatbot/backend/pyproject.toml backend/pyproject.toml


WORKDIR /app/backend

# installs uv
RUN pip install --no-cache-dir uv

# excluding packages that are marked as dev, e.g. black, ruff, flake8 ...
RUN uv sync --no-dev 

CMD ["uv", "run","uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]