import httpx

from app.model.dto.company_scraped_data_dto import CompanyScrapedDTO
from app.core.config import settings


class ScraperService:

    @staticmethod
    async def get_company_scraped_data(company_name: str) -> CompanyScrapedDTO:
        url = f"{settings.SCRAPER_BASE_URL}/api/scraper/company/{company_name}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return CompanyScrapedDTO(**response.json())
