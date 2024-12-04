from pydantic import BaseModel


class SearchDTO(BaseModel):
    company_name: str
