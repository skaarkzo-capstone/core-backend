from app.model.dto.search_dto import SearchDTO

def process_search(input_text: str) -> SearchDTO:
    return SearchDTO(companyName=input_text)
