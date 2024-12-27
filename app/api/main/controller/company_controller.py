from typing import List
from fastapi import APIRouter, HTTPException

from app.service.company_service import CompanyService
from app.service.scraper_service import ScraperService
from app.service.llm_service import LLMService
from app.model.dto.company_evaluated_dto import EvaluatedCompanyDTO
from app.model.request.company_request import CompanyRequest

router = APIRouter()


@router.get("/evaluated-companies", response_model=list[EvaluatedCompanyDTO])
async def get_all_evaluated_companies():
    return await CompanyService.get_all_evaluated_companies()


@router.post("/company")
async def get_company_scraped_data(search_request: CompanyRequest):

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
async def full_evaluation(search_request: CompanyRequest) -> EvaluatedCompanyDTO:
    try:
        scraped_company_data = await ScraperService.get_company_scraped_data(search_request)
        evaluated_company_data = await LLMService.evaluate_company(scraped_company_data)
        return evaluated_company_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=str(e)
        )
    
    
@router.delete("/delete-company")
async def delete_company(request: CompanyRequest):
    company = await CompanyService.get_evaluated_company(request.company_name)

    if not company:
        raise HTTPException(
            status_code=404, detail=f"Company '{request.company_name}' not found."
        )

    try:
        await CompanyService.delete_company(request.company_name)
        return {"message": "Company deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting company: {str(e)}"
        )


@router.delete("/delete-companies")
async def delete_companies(request: List[CompanyRequest]):
    failed_deletions = []
    success_deletions = []

    for company_request in request:
        try:
            company = await CompanyService.get_evaluated_company(company_request.company_name)
            if not company:
                failed_deletions.append(f"Company '{company_request.company_name}' not found.")
                continue

            await CompanyService.delete_company(company_request.company_name)
            success_deletions.append(company_request.company_name)
        except Exception as e:
            failed_deletions.append(f"Error deleting '{company_request.company_name}': {str(e)}")

    if failed_deletions:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Some companies could not be deleted.",
                "success": success_deletions,
                "failed": failed_deletions,
            },
        )

    return {
        "message": "All companies deleted successfully.",
        "success": success_deletions,
    }
