from typing import List
from fastapi import APIRouter, HTTPException

from app.service.company_service import CompanyService
from app.model.request.company_request import CompanyRequest
from bson import ObjectId

router = APIRouter()


@router.put("/company/compliance")
async def toggle_compliance(request: List[CompanyRequest]):
    company_ids = [company_request.id for company_request in request]
    valid_companies, failed_companies = await validate_and_fetch_companies(company_ids, include_compliance=True)

    successful_toggles = []

    try:
        for company in valid_companies:
            company_id = ObjectId(company["id"])

            # Toggle the compliance value
            new_compliance_status = await CompanyService.toggle_compliance(company_id, company["compliance"])

            successful_toggles.append({
                "id": str(company_id),
                "name": company["name"],
                "compliance": new_compliance_status
            })

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": f"An error occurred: {str(e)}",
                "success": successful_toggles,
                "failed": failed_companies,
            })

    return {
        "success": successful_toggles,
        "failed": failed_companies
    }


@router.delete("/delete-companies")
async def delete_companies(request: List[CompanyRequest]):
    company_ids = [company_request.id for company_request in request]
    valid_companies, failed_companies = await validate_and_fetch_companies(company_ids)

    try:

        # If there are valid companies to delete, pass them to the service
        if valid_companies:
            valid_company_ids = [ObjectId(company["id"]) for company in valid_companies]
            await CompanyService.delete_companies(valid_company_ids)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail={
                "message": f"An error occurred while deleting companies: {str(e)}",
                "success": valid_companies,
                "failed": failed_companies,
            },
        )

    return {
        "success": valid_companies,
        "failed": failed_companies
    }


async def validate_and_fetch_companies(company_ids: list, include_compliance: bool = False):
    valid_companies = []
    failed_companies = []

    for company_id in company_ids:
        try:
            if not ObjectId.is_valid(company_id):
                failed_companies.append({"id": str(company_id), "reason": f"400: Invalid ID - {company_id}"})
                continue

            # Fetch the company by ID
            company = await CompanyService.get_evaluated_company(ObjectId(company_id))

            if company:
                company_data = {
                    "id": str(company_id),
                    "name": company["name"]
                }

                # Include compliance if it's set to true
                if include_compliance:
                    company_data["compliance"] = company.get("compliance", False)

                valid_companies.append(company_data)
            else:
                failed_companies.append({"id": str(company_id), "reason": "404: Company not found"})

        except Exception as e:
            failed_companies.append({"id": str(company_id), "reason": f"500: An error occurred - {str(e)}"})

    return valid_companies, failed_companies
