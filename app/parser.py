from langchain_community.document_loaders import PyMuPDFLoader

def load_resume(pdf_path: str) -> str:
    loader = PyMuPDFLoader(pdf_path)

    documents = loader.load()

    for doc in documents:
        doc.metadata["resume_name"] = pdf_path.split("/")[-1]


    return documents