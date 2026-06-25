import os
from fastapi import (
    FastAPI,
    UploadFile,
    File,  
    HTTPException
)

from app.parser import extract_text
from app.schemas import ResumeResponse
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

    documents = extract_text(
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