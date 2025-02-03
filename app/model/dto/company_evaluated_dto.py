from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.model.dto.company_transactions_dto import TransactionDTO


class PurePlayReasoningDTO(BaseModel):
    green: str
    decarbonization: str
    social: str


class EvaluatedCompanyDTO(BaseModel):
    id: Optional[str] = None
    name: str
    date: datetime
    pure_play_reasoning: PurePlayReasoningDTO
    company_transactions: list[TransactionDTO] = []
    transaction_reasonings: list[str] = []
    compliance: bool
