FROM python:3.11-slim

# path inside of the container
WORKDIR /app

# copy workspace root files
COPY pyproject.toml uv.lock ./

#copy source
COPY src src

# installs uv
RUN pip install --no-cache-dir uv


# excluding packages that are marked as dev, e.g. black, ruff, flake8 ...
RUN uv sync --no-dev 

WORKDIR /app/src/mcf_rag_chatbot/backend

CMD ["uv", "run", "uvicorn", "mcf_rag_chatbot.backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
