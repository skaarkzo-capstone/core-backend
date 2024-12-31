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
    company_ids = [ObjectId(company_request.id) for company_request in request]
    failed_companies = []
    valid_companies = []

    for company_id in company_ids:
        try:
            if not ObjectId.is_valid(company_id):
                failed_companies.append({"id": company_id, "reason": f"Invalid ID: {company_id}"})
                raise HTTPException(status_code=400, detail=f"Invalid ID: {company_id}")
            # Fetch the company by ID
            company = await CompanyService.get_evaluated_company(company_id)
            if company:
                # Get the current compliance value
                current_compliance = company.get("compliance", False)

                # Toggle the compliance value
                new_compliance_status = await CompanyService.toggle_compliance(str(company_id), current_compliance)
                valid_companies.append({
                    "id": str(company_id),
                    "name": company["name"],
                    "compliance": new_compliance_status
                })
            else:
                failed_companies.append({"id": company_id, "reason": "Company not found"})
                raise HTTPException(status_code=404, detail=f"Company not found: {company_id}")
        except Exception as e:
            failed_companies.append({"id": company_id, "reason": str(e)})
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    try:
        return {
            "success": valid_companies,
            "failed": failed_companies
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": f"An error occurred while toggling compliance: {str(e)}",
                "success": valid_companies,
                "failed": failed_companies,
            },
        )


@router.delete("/delete-companies")
async def delete_companies(request: List[CompanyRequest]):
    company_ids = [ObjectId(company_request.id) for company_request in request]
    failed_companies = []
    valid_companies = []

    for company_id in company_ids:
        try:
            if not ObjectId.is_valid(company_id):
                failed_companies.append({"id": company_id, "reason": "Invalid ID: {company_id}"})
                raise HTTPException(status_code=400, detail=f"Invalid ID: {company_id}")
            # Fetch the company by ID
            company = await CompanyService.get_evaluated_company(company_id)
            if company:
                valid_companies.append({"id": str(company_id), "name": company["name"]})
            else:
                failed_companies.append({"id": company_id, "reason": "Company not found"})
                raise HTTPException(status_code=404, detail=f"Company not found: {company_id}")
        except Exception as e:
            failed_companies.append({"id": company_id, "reason": str(e)})
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    try:
        # If there are valid companies to delete, pass them to the service
        if valid_companies:
            valid_company_ids = [ObjectId(company["id"]) for company in valid_companies]
            await CompanyService.delete_companies(valid_company_ids)

        return {
            "success": valid_companies,
            "failed": failed_companies
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": f"An error occurred while deleting companies: {str(e)}",
                "success": valid_companies,
                "failed": failed_companies,
            },
        )
