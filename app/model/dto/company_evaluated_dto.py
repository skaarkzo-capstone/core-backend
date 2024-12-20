from pydantic import BaseModel
from datetime import datetime


class ReasoningDTO(BaseModel):
    green: str
    decarbonization: str
    social: str


class EvaluatedCompanyDTO(BaseModel):
    name: str
    date: datetime
    score: int
    reasoning: ReasoningDTO
