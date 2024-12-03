from pydantic import BaseModel
from datetime import datetime

class EvaluatedCompanyDTO(BaseModel):
    name: str
    date: datetime
    score: int
    reasoning: str
