from fastapi import APIRouter
from app.service.search_service import process_search
from app.model.dto.search_dto import SearchDTO
from app.model.request.search_request import SearchRequest

router = APIRouter()


@router.post("/", response_model=SearchDTO)
async def evaluate(request_body: SearchRequest):
    response = process_search(request_body.company_name)
    return response
