from app.model.dto.search_dto import SearchDTO


def process_search(input_text: str) -> SearchDTO:
    return SearchDTO(company_name=input_text)
