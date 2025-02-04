from pydantic import BaseModel
from typing import List


class ProductDTO(BaseModel):
    name: str
    description: str


class CompanyScrapedDTO(BaseModel):
    id: str
    name: str
    industry: str
    location: str
    type: str  # "Public" or "Private"
    size: str  # Number of employees or annual revenue
    annual_revenue: float
    market_cap: float
    key_products: List[ProductDTO]
    sustainability_goals: str
    social_goals: str
    governance: str
