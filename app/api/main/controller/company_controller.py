from fastapi import APIRouter
from app.service.company_service import CompanyService
from app.model.dto.company_dto import CompanyDTO

router = APIRouter()

@router.get("/companies", response_model=list[CompanyDTO])
async def get_all_companies():
    return await CompanyService.get_all_evaluated_companies()