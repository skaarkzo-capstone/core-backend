from app.model.dto.company_evaluated_dto import EvaluatedCompanyDTO
from app.db import database


class CompanyService:

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


    @staticmethod
    async def get_company(company_name: str) -> dict:
        companies_collection = database["companies"]
        company = await companies_collection.find_one({"name": company_name})

        return company


    @staticmethod
    async def toggle_compliance(company_name: str) -> dict:
        evaluated_companies_collection = database["evaluated_companies"]

        # Find the company
        company = await evaluated_companies_collection.find_one({"name": company_name})
        if not company:
            return None

        # Toggle the compliance value
        new_compliance_status = not company.get("compliance", False)

        # Update the database
        await evaluated_companies_collection.update_one(
            {"name": company_name},
            {"$set": {"compliance": new_compliance_status}}
        )

        # Fetch the updated company
        updated_company = await evaluated_companies_collection.find_one({"name": company_name})
        updated_company["_id"] = str(updated_company["_id"])
        return updated_company
