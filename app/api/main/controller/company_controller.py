from typing import List
from fastapi import APIRouter, HTTPException

from app.service.company_service import CompanyService
from app.service.scraper_service import ScraperService
from app.service.llm_service import LLMService
from app.model.dto.company_evaluated_dto import EvaluatedCompanyDTO
from app.model.request.company_request import CompanyRequest
from app.db import database
from bson import ObjectId
from app.service.company_service import CompanyService


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


@router.put("/company/compliance")
async def toggle_compliance(request: List[CompanyRequest]):
    evaluated_companies_collection = database["evaluated_companies"]
    failed_toggles = []
    success_toggles = []

    company_ids = [ObjectId(company_request.id) for company_request in request]

    try:
        for company_id in company_ids:
            try:
                # Find the company by ID
                company = await CompanyService.get_evaluated_company(company_id)
                if not company:
                    failed_toggles.append({"id": str(company_id), "reason": "Company not found"})
                    continue

                # Get the current compliance value
                current_compliance = company.get("compliance", False)

                # Toggle the compliance value
                new_compliance_status = await CompanyService.toggle_compliance(str(company_id), current_compliance)
                success_toggles.append({
                    "id": str(company_id),
                    "name": company["name"],
                    "compliance": new_compliance_status
                })
            except Exception as e:
                failed_toggles.append({"id": str(company_id), "reason": str(e)})

        return {
            "success": success_toggles,
            "failed": failed_toggles
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )


@router.delete("/delete-companies")
async def delete_companies(request: List[CompanyRequest]):
    company_ids = [ObjectId(company_request.id) for company_request in request]
    failed_deletions = []
    success_deletions = []

    try:
        for company_id in company_ids:
            try:
                # Fetch the company by ID
                company = await CompanyService.get_evaluated_company(company_id)
                if not company:
                    failed_deletions.append(f"Company with ID '{company_id}' not found.")
                    continue
                # Append a JSON object
                success_deletions.append({"name": company["name"], "id": str(company_id)})

            except Exception as e:
                failed_deletions.append(f"Error with ID '{company_id}': {str(e)}")

        # If there are valid companies to delete, pass them to the service
        if success_deletions:
            valid_company_ids = [ObjectId(company["id"]) for company in success_deletions]
            await CompanyService.delete_companies(valid_company_ids)

        return {
            "success": success_deletions,
            "failed": failed_deletions
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": f"An error occurred while deleting companies: {str(e)}",
                "success": success_deletions,
                "failed": failed_deletions,
            },
        )
