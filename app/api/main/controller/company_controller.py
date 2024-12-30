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

    try:
        for company_request in request:
            try:
                # Find the company by ID
                company = await evaluated_companies_collection.find_one({"_id": ObjectId(company_request.id)})
                if not company:
                    failed_toggles.append({"id": company_request.id, "reason": "Company not found"})
                    continue

                # Get the current compliance value
                current_compliance = company.get("compliance", False)

                # Toggle the compliance value
                new_compliance_status = await CompanyService.toggle_compliance(company_request.id, current_compliance)
                success_toggles.append({
                    "id": company_request.id,
                    "name": company["name"],
                    "compliance": new_compliance_status
                })
            except Exception as e:
                failed_toggles.append({"id": company_request.id, "reason": str(e)})

        # Construct a response message
        if len(success_toggles) == 1:
            message = f"Compliance for company '{success_toggles[0]['name']}' with ID '{success_toggles[0]['id']}' updated successfully."
        elif len(success_toggles) > 1:
            companies_list = ", ".join(
                [f"{company['name']} with ID {company['id']}" for company in success_toggles[:-1]]
            )
            last_company = f"{success_toggles[-1]['name']} with ID {success_toggles[-1]['id']}"
            message = f"Compliance for companies {companies_list}, and {last_company} updated successfully."
        else:
            message = "No companies were updated."

        # Return the response
        return {
            "message": message,
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
        # Fetch all companies to validate existence
        for company_id in company_ids:
            company = await CompanyService.get_evaluated_company(company_id)
            if not company:
                failed_deletions.append(f"Company with ID '{company_id}' not found.")
                continue
            # Append a tuple of company name and ID
            success_deletions.append((company["name"], str(company_id)))

        # If there are valid companies to delete, pass them to the service
        if success_deletions:
            await CompanyService.delete_companies(company_ids)

        # Message set dynamically
        if len(success_deletions) == 1:
            message = (
                f"Company {success_deletions[0][0]} with ID {success_deletions[0][1]} was deleted."
            )
        elif len(success_deletions) > 1:
            companies_list = ", ".join(
                [f"{name} with ID {cid}" for name, cid in success_deletions[:-1]]
            )
            last_company = f"{success_deletions[-1][0]} with ID {success_deletions[-1][1]}"
            message = f"Companies {companies_list}, and {last_company} were deleted."
        else:
            message = "No companies were deleted."

        # Return response with successful and failed deletions
        return {
            "message": message,
            "success": [
                {"name": name, "id": cid} for name, cid in success_deletions
            ],
            "failed": failed_deletions,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": f"An error occurred while deleting companies: {str(e)}",
                "success": [
                    {"name": name, "id": cid} for name, cid in success_deletions
                ],
                "failed": failed_deletions,
            },
        )
