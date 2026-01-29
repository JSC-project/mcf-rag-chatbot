from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_PATH = PROJECT_ROOT / "data" / "data_from_crawler"


VECTOR_DATABASE_PATH = PROJECT_ROOT / "knowledge_base"

#Name on table inside db.
TABLE_NAME = "mcf_content"