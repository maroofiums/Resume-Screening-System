import os
from fastapi import (
    FastAPI,
    UploadFile,
    File,  
    HTTPException
)

from app.parser import extract_text
from app.schemas import ResumeResponse

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

@app.post("/upload", response_model=ResumeResponse)
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

    extracted_text = extract_text(
        str(file_path)
    )

    print(extracted_text)

    return ResumeResponse(
        filename=filename,
        text_length=len(extracted_text),
        extracted_text=extracted_text
    )