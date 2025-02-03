from pydantic import BaseModel
from typing import Optional


class TransactionDTO(BaseModel):
    id: Optional[str] = None
    purpose: str
    context: str
    value: int


class CompanyTransactionsDTO(BaseModel):
    name: str
    transactions: list[TransactionDTO]
