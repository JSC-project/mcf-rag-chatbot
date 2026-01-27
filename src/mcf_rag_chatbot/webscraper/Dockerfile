FROM python:3.13-slim

# path inside of the container
WORKDIR /app/webscraper

# later in docker compose, we'll use a context that is parent of frontend folder
# then we can send in the frontend folder by writing frontend
COPY src/mcf_rag_chatbot/webscraper .
COPY pyproject.toml uv.lock ./
COPY src/mcf_rag_chatbot/backend/pyproject.toml backend/pyproject.toml


# installs uv
RUN pip install --no-cache-dir uv

# excluding packages that are marked as dev, e.g. black, ruff, flake8 ...
RUN uv sync --no-dev 

CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]