from pathlib import Path

from langchain_community.vectorstores import FAISS

VECTOR_DB_PATH = "vector_db"

def save_documents(documents, embeddings):
    db = FAISS.from_documents(
        documents,
        embeddings
    )

    db.save_local(
        VECTOR_DB_PATH
    )

    return db

def load_vector_store(embeddings):
    path = Path(VECTOR_DB_PATH)

    if not path.exists():
        return None

    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )