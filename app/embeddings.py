import os

from dotenv import load_dotenv
from langchain_mistralai import MistralAIEmbeddings

load_dotenv()

embeddings = MistralAIEmbeddings(
    model="mistral-embed",
    api_key=os.getenv("MISTRAL_API_KEY")
)