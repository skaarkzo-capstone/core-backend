from pydantic import BaseModel
from datetime import datetime


class ReasoningDTO(BaseModel):
    green: str
    decarbonization: str
    social: str


class EvaluatedCompanyDTO(BaseModel):
    id: str
    name: str
    date: datetime
    score: int
    reasoning: ReasoningDTO
    compliance: bool
