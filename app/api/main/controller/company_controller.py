from fastapi import APIRouter, HTTPException

from app.service.company_service import CompanyService
from app.service.scraper_service import ScraperService
from app.service.llm_service import LLMService
from app.model.dto.company_evaluated_dto import EvaluatedCompanyDTO
from app.model.request.search_request import SearchRequest
from app.db import database

router = APIRouter()


@router.get("/evaluated-companies", response_model=list[EvaluatedCompanyDTO])
async def get_all_evaluated_companies():
    return await CompanyService.get_all_evaluated_companies()


@router.post("/company")
async def get_company_scraped_data(search_request: SearchRequest):

    # TODO: Uncomment when companies are added to DB.
    # company = await CompanyService.get_company(search_request.companyName)

    # if not company:
    #     raise HTTPException(
    #         status_code=404, detail={"error": f"Company '{search_request.company_name}' not found."}
    #     )

    try:
        scraped_company_data = await ScraperService.get_company_scraped_data(search_request)
        return scraped_company_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail={"error": str(e)}
        )


@router.post("/company/evaluate")
async def get_company_evaluation(scraped_company_data: dict) -> EvaluatedCompanyDTO:
    try:
        evaluated_company_data = await LLMService.evaluate_company(scraped_company_data)
        return evaluated_company_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=str(e)
        )


@router.post("/complete-evaluation")
async def full_evaluation(search_request: SearchRequest) -> EvaluatedCompanyDTO:
    try:
        scraped_company_data = await ScraperService.get_company_scraped_data(search_request)
        evaluated_company_data = await LLMService.evaluate_company(scraped_company_data)
        return evaluated_company_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=str(e)
        )
    

@router.put("/company/compliance")
async def toggle_compliance(request: SearchRequest):
    evaluated_companies_collection = database["evaluated_companies"]

    # Find the company
    company = await evaluated_companies_collection.find_one({"name": request.company_name})
    if not company:
        raise HTTPException(
            status_code=404, detail=f"Company '{request.company_name}' not found."
        )

    # Get the current compliance value
    current_compliance = company.get("compliance", False)

    try:
        await CompanyService.toggle_compliance(request.company_name, current_compliance)
        return {
            "message": f"Compliance for '{request.company_name}' updated successfully.",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=str(e)
        )
