# Resume Screening System

## Overview

Resume Screening System is an AI-powered application that helps recruiters identify the most suitable candidates for a job description. It leverages Large Language Model (LLM) embeddings and semantic search to compare resumes against job requirements.

Instead of relying solely on keyword matching, the system understands the semantic meaning of resumes and job descriptions using Mistral embeddings and FAISS vector search.

---

# Features

* Upload resume PDFs
* Extract text from resumes
* Generate semantic embeddings using Mistral AI
* Store embeddings in a FAISS vector database
* Search resumes using natural language
* Rank resumes based on job descriptions
* FastAPI REST API with interactive Swagger documentation

---

# Tech Stack

## Backend

* FastAPI
* Python

## AI / NLP

* LangChain
* Mistral AI Embeddings
* FAISS

## Document Processing

* PyMuPDF
* LangChain Document Loaders

## Validation

* Pydantic

---

# Project Structure

```text
resume-screening-system/

├── app/
│   ├── main.py
│   ├── parser.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── ranking.py
│   └── schemas.py
│
├── resumes/
│
├── vector_db/
│
├── .env
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository.

```bash
git clone https://github.com/maroofiums/Resume-Screening-System.git
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```env
MISTRAL_API_KEY=your_api_key_here
```

---

# Run the Application

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Home

### GET /

Returns a welcome message.

---

## Upload Resume

### POST /upload

Uploads a PDF resume and indexes it into the FAISS vector database.

Supported format:

* PDF

Example Response

```json
{
    "message": "Resume indexed successfully",
    "filename": "resume.pdf",
    "pages": 2
}
```

---

## Search Resume

### GET /search

Search indexed resumes using natural language.

Example

```
/search?query=FastAPI Developer
```

Example Response

```json
{
    "results": [
        "...Python FastAPI Docker...",
        "...REST API development..."
    ]
}
```

---

## Rank Candidates

### POST /rank

Ranks resumes according to a job description.

Example Request

```json
{
    "description": "Looking for a Machine Learning Engineer with Python, FastAPI, Docker, SQL and LangChain."
}
```

Example Response

```json
[
    {
        "resume": "resume.pdf",
        "score": 94.81,
        "page": 0,
        "preview": "Experienced Machine Learning Engineer..."
    }
]
```

---

# Workflow

```
Resume PDF
      │
      ▼
PyMuPDF Loader
      │
      ▼
LangChain Documents
      │
      ▼
Mistral Embeddings
      │
      ▼
FAISS Vector Store
      │
      ├──────────────► Semantic Search
      │
      └──────────────► Resume Ranking
                              │
                              ▼
                      Ranked Candidates
```

---

# Current Features

* PDF resume upload
* Resume parsing
* Semantic embeddings
* FAISS indexing
* Resume retrieval
* Candidate ranking

---

# Planned Features

* Skill extraction
* ATS score calculation
* Candidate profile extraction
* Experience analysis
* Education extraction
* Recruiter-friendly AI explanations
* PostgreSQL integration
* Authentication and user management
* Streamlit dashboard
* Docker deployment
* CI/CD pipeline
* Unit and integration testing

---

# Future Improvements

* Support DOCX resumes
* Batch resume uploads
* Hybrid ranking (semantic + keyword)
* Resume deduplication
* Recruiter dashboard
* Resume analytics
* Multi-language support
* Cloud deployment
* Vector database migration (Qdrant, Chroma, or Pinecone)

---

# License

This project is intended for educational and portfolio purposes.
