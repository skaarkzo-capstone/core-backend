import httpx
from fastapi import HTTPException

from app.model.request.search_request import SearchRequest
from app.core.config import settings


class ScraperService:

    @staticmethod
    async def get_company_scraped_data(search_request: SearchRequest):
        url = f"{settings.SCRAPER_BASE_URL}/api/scraper/company/"

        async with httpx.AsyncClient(timeout=settings.MAX_TIMEOUT) as client:
            try:
                response = await client.post(url, json=search_request.dict())
                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as e:

                if e.response.status_code == 404:
                    raise HTTPException(status_code=e.response.status_code,
                                        detail=f"Company data not found for: {search_request.company_name}")

                raise HTTPException(status_code=e.response.status_code,
                                    detail=f"Data Scraper Service returned an unexpected error: "
                                           f"{e.response.status_code} Error")

            except httpx.TimeoutException as e:

                raise HTTPException(status_code=500,
                                    detail=f"Couldn't receive response from Data Scraper Service on time.")

            except Exception as e:

                raise HTTPException(status_code=500,
                                    detail="An unexpected error occurred trying to reach the Data Scraper Service. "
                                           "Please try again later.")

