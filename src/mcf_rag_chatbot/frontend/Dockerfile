FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

COPY src/mcf_rag_chatbot/frontend frontend

RUN pip install --no-cache-dir uv

RUN uv sync --no-dev

WORKDIR /app/frontend

CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
