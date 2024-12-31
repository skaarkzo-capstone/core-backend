from pydantic import BaseModel
from typing import Optional


class CompanyRequest(BaseModel):
    id: Optional[str] = None
    company_name: str = ""
    website: bool = True    # Default value set as true
    sedar: bool = True      # Default value set as true
