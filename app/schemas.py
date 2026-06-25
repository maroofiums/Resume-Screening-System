from pydantic import BaseModel

class ResumeResponse(BaseModel):
    filename: str
    text_length: int
    extracted_text: str