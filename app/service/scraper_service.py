import httpx
from fastapi import HTTPException

from app.model.dto.company_scraped_data_dto import CompanyScrapedDTO
from app.core.config import settings


class ScraperService:

    @staticmethod
    async def get_company_scraped_data(company_name: str):
        url = f"{settings.SCRAPER_BASE_URL}/api/scraper/company/{company_name}"

        async with httpx.AsyncClient() as client:
            try:

                response = await client.get(url)
                response.raise_for_status()
                return CompanyScrapedDTO(**response.json())

            except httpx.HTTPStatusError as e:

                if e.response.status_code == 404:
                    raise HTTPException(status_code=e.response.status_code,
                                        detail={"error": f"Company data not found for: {company_name}"})

                raise HTTPException(status_code=e.response.status_code,
                                    detail={"error": f"Data Scraper Service returned an unexpected error: "
                                                     f"{e.response.status_code} Error"})

            except Exception as e:

                raise HTTPException(status_code=500,
                                    detail={"error": "An unexpected error occurred trying to reach "
                                                     "the Data Scraper Service. Please try again later."})

