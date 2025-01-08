import httpx
import asyncio
from fastapi import HTTPException, Request

from app.model.dto.company_evaluated_dto import EvaluatedCompanyDTO
from app.core.config import config
from app.db import database


class LLMService:

    @staticmethod
    async def evaluate_company(scraped_data: dict, request: Request) -> EvaluatedCompanyDTO:
        url = config.llm_service.EVALUATE_COMPANY
        evaluated_companies_collection = database["evaluated_companies"]

        async with httpx.AsyncClient(timeout=config.MAX_TIMEOUT) as client:
            try:
                task = asyncio.create_task(
                    client.post(url, json=scraped_data)
                )

                while not task.done():
                    if await request.is_disconnected():
                        task.cancel()
                        raise HTTPException(status_code=499, detail="Client disconnected during request.")

                    await asyncio.sleep(0.1)  # Cancellation checks (non-blocking delay)

                response = await task
                response.raise_for_status()

                await evaluated_companies_collection.insert_one(response.json())
                return EvaluatedCompanyDTO(**response.json())

            except asyncio.CancelledError as e:
                raise HTTPException(status_code=499, detail="Evaluation request was cancelled.")

            except httpx.HTTPStatusError as e:

                raise HTTPException(status_code=e.response.status_code,
                                    detail=f"LLM Service returned an unexpected error: {e.response.text}")

            except httpx.TimeoutException as e:

                raise HTTPException(status_code=500,
                                    detail=f"Couldn't receive response from LLM Service on time.")

            except Exception as e:

                raise HTTPException(status_code=500,
                                    detail="An unexpected error occurred trying to reach the LLM Service. "
                                           "Please try again later.")
