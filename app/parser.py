from langchain_community.document_loaders import PyMuPDFLoader

def extract_text(pdf_path: str) -> str:
    loader = PyMuPDFLoader(pdf_path)

    documents = loader.load()

    return documents