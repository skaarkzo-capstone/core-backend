from fastapi import APIRouter
from app.service.company_service import CompanyService
from app.service.scraper_service import ScraperService
from app.model.dto.company_evaluated_dto import CompanyDTO
from app.model.dto.company_scraped_data_dto import CompanyScrapedDTO

router = APIRouter()


@router.get("/companies", response_model=list[CompanyDTO])
async def get_all_companies():
    return await CompanyService.get_all_evaluated_companies()


@router.get("/company/{company_name}", response_model=CompanyScrapedDTO)
async def get_company_scraped_data(company_name: str):
    scraped_company_data = await ScraperService.get_company_scraped_data(company_name)
    return scraped_company_data
