from pydantic import BaseModel

class SearchDTO(BaseModel):
    companyName: str
