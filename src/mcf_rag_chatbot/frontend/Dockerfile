FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY src src

RUN pip install --no-cache-dir uv
RUN uv sync --no-dev

WORKDIR /app/src/mcf_rag_chatbot/webscraper

CMD ["uv", "run", "-m", "mcf_rag_chatbot.webscraper.mcf_scraper"]

