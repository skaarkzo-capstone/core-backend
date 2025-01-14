from typing import List
from app.model.dto.company_evaluated_dto import EvaluatedCompanyDTO
from app.db import database
from bson import ObjectId
from fastapi import HTTPException
import httpx


class CompanyService:

    # Fetch a company document by its MongoDB ObjectId
    @staticmethod
    async def get_evaluated_company(company_id: ObjectId):
        evaluated_companies_collection = database["evaluated_companies"]

        try:
            return await evaluated_companies_collection.find_one({"_id": company_id})

        except httpx.HTTPStatusError as e:

            if e.response.status_code == 404:
                raise HTTPException(status_code=e.response.status_code,
                                    detail=f"Unable to find company with ID {company_id}")

        except Exception as e:

            raise HTTPException(status_code=500,
                                detail=f"Error fetching company with ID {company_id}: {e}")

    # Get all the evaluated companies
    @staticmethod
    async def get_all_evaluated_companies() -> list[EvaluatedCompanyDTO]:
        # Get all the documents (rows) from the collection
        evaluated_companies_collection = database["evaluated_companies"]
        documents = evaluated_companies_collection.find({})

        # Convert documents to CompanyDTOs
        companies = []
        async for document in documents:
            # MongoDB's ObjectId to a string
            document["id"] = str(document.pop("_id"))

            # ** unpacks the document dictionary and maps each k/v pair to the correct CompanyDTO field.
            company = EvaluatedCompanyDTO(**document)
            companies.append(company)

        return companies

    # Toggle the compliance of the companies
    @staticmethod
    async def toggle_compliance(company_id: ObjectId, current_compliance: bool) -> bool:
        evaluated_companies_collection = database["evaluated_companies"]

        # Toggle the compliance value
        new_compliance_status = not current_compliance

        # Update the database
        result = await evaluated_companies_collection.update_one(
            {"_id": company_id},
            {"$set": {"compliance": new_compliance_status}}
        )

        # Check if the update was successful
        if result.modified_count == 1:
            updated_company = await evaluated_companies_collection.find_one({"_id": company_id})
            if updated_company and updated_company.get("compliance") == new_compliance_status:
                return new_compliance_status

        raise HTTPException(status_code=500, detail="An error occurred: Failed to toggle compliance")

    # Delete the companies
    @staticmethod
    async def delete_companies(company_ids: List[ObjectId]):
        evaluated_companies_collection = database["evaluated_companies"]

        try:
            await evaluated_companies_collection.delete_many({"_id": {"$in": company_ids}})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting companies: {e}")
