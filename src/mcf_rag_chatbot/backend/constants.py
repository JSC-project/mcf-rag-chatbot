from pathlib import Path

DATA_PATH = Path(__file__).parents[3] / "webscraper" / "data"

VECTOR_DATABASE_PATH = Path(__file__).parents[2] / "knowledge_base"

#Name on table inside db.
TABLE_NAME = "mcf_content"