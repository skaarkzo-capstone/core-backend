import asyncio
from fastapi import APIRouter, HTTPException, Request

from app.service.company_service import CompanyService
from app.service.scraper_service import ScraperService
from app.service.llm_service import LLMService
from app.model.dto.company_evaluated_dto import EvaluatedCompanyDTO
from app.model.request.company_request import CompanyRequest

router = APIRouter()

@router.get("/evaluated-companies", response_model=list[EvaluatedCompanyDTO])
async def get_all_evaluated_companies():
    try:
        return await CompanyService.get_all_evaluated_companies()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}"
        )


@router.post("/company")
async def get_company_scraped_data(search_request: CompanyRequest, request: Request):
    # TODO: Uncomment when companies are added to DB.
    # company = await CompanyService.get_company(search_request.companyName)

    # if not company:
    #     raise HTTPException(
    #         status_code=404, detail={"error": f"Company '{search_request.company_name}' not found."}
    #     )

    try:
        scraped_company_data = await ScraperService.get_company_scraped_data(search_request, request)

        if await request.is_disconnected():
            raise HTTPException(status_code=499, detail="Client disconnected during processing.")

        return scraped_company_data

    except asyncio.CancelledError as e:
        raise HTTPException(status_code=499, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}"
        )


@router.post("/company/evaluate")
async def get_company_evaluation(scraped_company_data: dict) -> EvaluatedCompanyDTO:
    try:
        evaluated_company_data = await LLMService.evaluate_company(scraped_company_data)
        return evaluated_company_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}"
        )


@router.post("/complete-evaluation")
async def full_evaluation(search_request: CompanyRequest, request: Request) -> EvaluatedCompanyDTO:
    try:

        scraped_company_data = await ScraperService.get_company_scraped_data(search_request, request)

        if await request.is_disconnected():
            raise HTTPException(status_code=499, detail="Client disconnected during processing.")

        evaluated_company_data = await LLMService.evaluate_company(scraped_company_data)

        if await request.is_disconnected():
            raise HTTPException(status_code=499, detail="Client disconnected during processing.")

        return evaluated_company_data

    except asyncio.CancelledError as e:
        raise HTTPException(status_code=499, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}"
        )
