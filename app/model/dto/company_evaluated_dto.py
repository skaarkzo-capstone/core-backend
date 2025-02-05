from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.model.dto.company_transactions_dto import EvaluatedTransactionDTO


class EvaluatedCompanyDTO(BaseModel):
    id: Optional[str] = None
    name: str
    date: datetime
    pure_play: bool
    pure_play_reasoning: str
    evaluated_transactions: list[EvaluatedTransactionDTO] = []
