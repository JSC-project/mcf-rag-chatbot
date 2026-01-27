import lancedb 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .constants import VECTOR_DATABASE_PATH, TABLE_NAME
from .data_models import MCFContent


def get_db():
    VECTOR_DATABASE_PATH.mkdir(parents=True, exist_ok=True)
    #Connects to Lancedb at the location we determined in constants.py
    return lancedb.connect(str(VECTOR_DATABASE_PATH))

def init_table():
    #Open Table or creating it if not exist
    db = get_db()
    tables_resp = db.list_tables()
    tables = tables_resp.tables
    

    print("DB URI:", str(VECTOR_DATABASE_PATH))
    print("Existing tables:", tables)
    print("TABLE_NAME:", TABLE_NAME)

    if TABLE_NAME not in tables:
        #Here the table is created with MCFContent as model
        return db.create_table(TABLE_NAME, schema=MCFContent)
    return db.open_table(TABLE_NAME)

def ingest_raw_content(url: str, title: str, raw_text: str):
    #1. Splits the text in chunks
    #2. Creates MCFContent-objekt
    #3. Saves them in LanceDB (that handles embeddings automatically)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = text_splitter.split_text(raw_text)

    #Creates list with object for each chunk
    documents = [
        MCFContent(url=url, title=title, content=chunk)
        for chunk in chunks
    ]

    # Saves in db
    table = init_table()
    table.add(documents)
    
def search_knowledge_base(query: str, limit: int = 3):
    "Serach for most relevent texts based on the question."
    table = init_table()
    
    #LanceDB converts your text query into a vector and searches the database
    results = table.search(query).limit(limit).to_pydantic(MCFContent)
    return results

if __name__ == "__main__":
    print("DB path:", VECTOR_DATABASE_PATH.resolve())
    table = init_table()
    print("Row count:", table.count_rows())
    print("OK: knowledge_base initialized")