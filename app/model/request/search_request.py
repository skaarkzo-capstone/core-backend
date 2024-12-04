from pydantic import BaseModel


class SearchRequest(BaseModel):
    company_name: str
    website: bool
    sedar: bool
