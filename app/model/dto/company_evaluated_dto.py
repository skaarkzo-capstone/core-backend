from pydantic import BaseModel
from datetime import datetime

class CompanyDTO(BaseModel):
    id: str
    name: str
    date: datetime
    score: int
    reasoning: str
