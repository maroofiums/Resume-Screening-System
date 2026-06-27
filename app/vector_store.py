from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy

VECTOR_DB_PATH = "vector_db"


def save_documents(documents, embeddings):
    """
    Save documents to FAISS.
    If the index already exists, append new documents.
    Otherwise, create a new index.
    """

    path = Path(VECTOR_DB_PATH)

    if path.exists():
        db = FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        db.add_documents(documents)

    else:
        db = FAISS.from_documents(
            documents,
            embeddings,
            distance_strategy = DistanceStrategy.COSINE
        )

    db.save_local(VECTOR_DB_PATH)

    return db


def load_vector_store(embeddings):
    """
    Load the existing FAISS vector store.
    """

    path = Path(VECTOR_DB_PATH)

    if not path.exists():
        return None

    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
        distance_strategy = DistanceStrategy.COSINE
    )