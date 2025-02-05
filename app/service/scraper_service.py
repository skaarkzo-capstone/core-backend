import httpx
import asyncio
from fastapi import HTTPException, Request

from app.model.request.company_request import CompanyRequest
from app.core.config import config


class ScraperService:

    @staticmethod
    async def get_company_scraped_data(company_request: CompanyRequest, request: Request):
        url = config.data_scraper_service.SCRAPE_COMPANY

        async with httpx.AsyncClient(timeout=config.MAX_TIMEOUT) as client:
            try:
                task = asyncio.create_task(
                    client.post(url, json=company_request.dict())
                )

                while not task.done():
                    if await request.is_disconnected():
                        task.cancel()
                        raise HTTPException(status_code=499, detail="Client disconnected during request.")

                    await asyncio.sleep(0.1)    # Cancellation checks (non-blocking delay)

                response = await task
                response.raise_for_status()

                non_pdf_scraped_data = ScraperService.traverse_and_remove_pdfs(response.json())
                return non_pdf_scraped_data
                # return response.json()

            except asyncio.CancelledError:
                raise HTTPException(status_code=499, detail="Evaluation request was cancelled.")

            except httpx.HTTPStatusError as e:

                if e.response.status_code == 404:
                    raise HTTPException(status_code=e.response.status_code,
                                        detail=f"Company data not found for: {company_request.company_name}")

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

