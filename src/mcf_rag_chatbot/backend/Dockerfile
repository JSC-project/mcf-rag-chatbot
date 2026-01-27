FROM python:3.13-slim

# path inside of the container
WORKDIR /app

# copy workspace root files
COPY pyproject.toml uv.lock ./

# copy backend 
COPY src/mcf_rag_chatbot/backend backend

# installs uv
RUN pip install --no-cache-dir uv

# excluding packages that are marked as dev, e.g. black, ruff, flake8 ...
RUN uv sync --no-dev 

WORKDIR /app/backend

CMD ["uv", "run","uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]