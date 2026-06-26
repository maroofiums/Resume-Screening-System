from pydantic import BaseModel


class JobDescription(BaseModel):
    description: str


class RankedResume(BaseModel):
    resume: str
    score: float
    page: int
    preview: str