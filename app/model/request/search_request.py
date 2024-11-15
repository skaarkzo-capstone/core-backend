from pydantic import BaseModel

class SearchRequest(BaseModel):
    companyName: str