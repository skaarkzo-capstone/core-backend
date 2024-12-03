from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.service.company_service import CompanyService
from app.service.scraper_service import ScraperService
from app.model.dto.company_evaluated_dto import CompanyDTO
from app.model.request.search_request import SearchRequest

router = APIRouter()


@router.get("/companies", response_model=list[CompanyDTO])
async def get_all_companies():
    return await CompanyService.get_all_evaluated_companies()


@router.post("/company")
async def get_company_scraped_data(search_request: SearchRequest):

    # TODO: Uncomment when companies are added to DB.
    # company = await CompanyService.get_company(search_request.companyName)

    # if not company:
    #     raise HTTPException(
    #         status_code=404, detail={"error": f"Company '{search_request.companyName}' not found."}
    #     )

    try:
        scraped_company_data = await ScraperService.get_company_scraped_data(search_request)
        return scraped_company_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail={"error": str(e)}
        )
