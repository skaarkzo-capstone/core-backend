from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReasoningDTO(BaseModel):
    green: str
    decarbonization: str
    social: str


class EvaluatedCompanyDTO(BaseModel):
    id: Optional[str] = None
    name: str
    date: datetime
    score: int
    reasoning: ReasoningDTO
    compliance: bool
