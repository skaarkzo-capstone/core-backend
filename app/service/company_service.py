from app.model.dto.company_evaluated_dto import CompanyDTO
from app.db import database


class CompanyService:

    @staticmethod
    async def get_all_evaluated_companies() -> list[CompanyDTO]:
        # Get all the documents (rows) from the collection
        evaluated_companies_collection = database["evaluated_companies"]
        documents = evaluated_companies_collection.find({})

        # Convert documents to CompanyDTOs
        companies = []
        async for document in documents:
            # MongoDB's ObjectId to a string
            document["id"] = str(document.pop("_id"))

            # ** unpacks the document dictionary and maps each k/v pair to the correct CompanyDTO field.
            company = CompanyDTO(**document)
            companies.append(company)

        return companies

    @staticmethod
    async def get_company(company_name: str) -> dict:
        companies_collection = database["companies"]
        company = await companies_collection.find_one({"name": company_name})

        return company
