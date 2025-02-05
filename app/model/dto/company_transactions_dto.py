from pydantic import BaseModel


class TransactionDTO(BaseModel):
    purpose: str
    context: str
    value: int


# Database Schema for a Company's Transaction
class CompanyTransactionsDTO(BaseModel):
    name: str
    transactions: list[TransactionDTO]


class EvaluatedTransactionDTO(BaseModel):
    purpose: str
    context: str
    value: int
    compliance: bool
    transaction_reasoning: str

