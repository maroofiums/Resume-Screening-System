from pathlib import Path
import os, shutil
from fastapi import (
    FastAPI,
    UploadFile,
    File,  
    HTTPException
)

from app.config import *
from app.ranking import rank_resumes
from app.schemas import JobDescription
from app.parser import load_resume
from app.embeddings import embeddings
from app.vector_store import (
    load_vector_store,
    save_documents
)

app = FastAPI(
    title="Resume Screening System"
)

UPLOAD_DIR = "resumes"
os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

@app.get("/")
def home():
    return {
        "message": "Welcome to Resume Screening System..."
    }

@app.post("/upload")
async def upload_resume(
    file: UploadFile = File(...)
):
    
    filename = file.filename

    if not filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files allowed"
        )
    
    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    documents = load_resume(
        str(file_path)
    )

    save_documents(
        documents,
        embeddings
    )

    return {
        "message": "Resume indexed successfully",
        "filename": file.filename,
        "pages": len(documents)
    }

@app.get("/search")
def search_resume(
    query: str
):
    db = load_vector_store(embeddings)

    if db is None:
        raise HTTPException(status_code=404,detail="No resumes indexed")

    docs = db.similarity_search(
        query,
        k=3
    )

    return {
        "results": [
            doc.page_content
            for doc in docs
        ]
    }

@app.post("/rank")
def rank_candidates(
    job: JobDescription
):

    db = load_vector_store(
        embeddings
    )

    if db is None:
        return {
            "error": "No resumes found."
        }

    ranked = rank_resumes(
        db,
        job.description
    )

    return ranked



@app.get("/resumes")
def list_resumes():
    files = os.listdir(UPLOAD_DIR)
    pdfs = [f for f in files if f.endswith(".pdf")]

    return {
        "total": len(pdfs),
        "resumes": pdfs
    }


@app.delete("/resumes/{filename}")
def delete_resume(filename: str):
    file_path = Path(UPLOAD_DIR) / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"{filename} not found"
        )

    os.remove(file_path)

    return {
        "message": f"{filename} deleted from disk",
        "note": "Re-index required. Call POST /reindex to rebuild the vector store."
    }


@app.post("/reindex")
def reindex_all():
    """
    Wipe the vector store and re-index all PDFs currently in the resumes/ folder.
    Call this after deleting a resume.
    """
    # Clear existing vector store
    if Path(VECTOR_DB_PATH).exists():
        shutil.rmtree(VECTOR_DB_PATH)

    pdfs = list(Path(UPLOAD_DIR).glob("*.pdf"))

    if not pdfs:
        return {"message": "No resumes found to index"}

    all_documents = []

    for pdf_path in pdfs:
        docs = load_resume(str(pdf_path))
        all_documents.extend(docs)

    save_documents(all_documents, embeddings)

    return {
        "message": "Reindex complete",
        "resumes_indexed": [p.name for p in pdfs]
    }