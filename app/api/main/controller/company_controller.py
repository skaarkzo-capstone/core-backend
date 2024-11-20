from fastapi import APIRouter, HTTPException

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
    company = await CompanyService.get_company(company_name)

    if not company:
        raise HTTPException(
            status_code=404, detail={"error": f"Company '{company_name}' not found."}
        )

    try:
        scraped_company_data = await ScraperService.get_company_scraped_data(company_name)
        return scraped_company_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail={"error": "An unexpected error occurred while processing your request."}
        )
