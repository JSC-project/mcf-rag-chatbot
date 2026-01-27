FROM python:3.13-slim

WORKDIR /app

COPY src/mcf_rag_chatbot/webscraper .
COPY pyproject.toml uv.lock ./

# installs uv
RUN pip install --no-cache-dir uv

# excluding packages that are marked as dev, e.g. black, ruff, flake8 ...
RUN uv sync --no-dev 

WORKDIR /app/webscraper

CMD ["uv", "run", "-m", "mcf_rag_chatbot.webscraper.mcf_scraper"]