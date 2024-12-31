import httpx
from fastapi import HTTPException

from app.model.request.company_request import CompanyRequest
from app.core.config import config


class ScraperService:

    @staticmethod
    async def get_company_scraped_data(search_request: CompanyRequest):
        url = config.data_scraper_service.SCRAPE_COMPANY

        async with httpx.AsyncClient(timeout=config.MAX_TIMEOUT) as client:
            try:
                response = await client.post(url, json=search_request.dict())
                response.raise_for_status()

                non_pdf_scraped_data = ScraperService.traverse_and_remove_pdfs(response.json())
                return non_pdf_scraped_data
                # return response.json()

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

    # TODO: Remove once data normalization is complete
    @staticmethod
    def traverse_and_remove_pdfs(scraped_data: dict):
        if isinstance(scraped_data, dict):
            for key, value in scraped_data.items():
                if key == "pdfs":
                    scraped_data[key] = []
                else:
                    ScraperService.traverse_and_remove_pdfs(value)
        elif isinstance(scraped_data, list):
            for item in scraped_data:
                ScraperService.traverse_and_remove_pdfs(item)

        return scraped_data

