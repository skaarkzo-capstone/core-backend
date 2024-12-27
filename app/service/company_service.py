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
    async def get_evaluated_company(company_name: str) -> dict:
        evaluated_companies_collection = database["evaluated_companies"]
        company = await evaluated_companies_collection.find_one({"name": company_name})

        return company


    @staticmethod
    async def delete_company(company_name: str):
        evaluated_companies_collection = database["evaluated_companies"]
        try:
            await evaluated_companies_collection.delete_one({"name": company_name})
        except Exception as e:
            raise Exception(f"Error deleting company: {e}")
