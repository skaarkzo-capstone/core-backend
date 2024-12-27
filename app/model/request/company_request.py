from pydantic import BaseModel


class CompanyRequest(BaseModel):
    company_name: str
    website: bool = True    # Default value set as true
    sedar: bool = True      # Default value set as true
