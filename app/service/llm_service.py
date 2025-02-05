import httpx
import asyncio
from fastapi import HTTPException, Request

from app.model.dto.company_evaluated_dto import EvaluatedCompanyDTO
from app.core.config import config
from app.db import database
from app.model.request.company_request import CompanyRequest
from app.service.company_service import CompanyService


class LLMService:

    @staticmethod
    async def evaluate_company(scraped_data: dict, company_request: CompanyRequest,
                               request: Request) -> EvaluatedCompanyDTO:
        url_pure_play = config.llm_service.EVALUATE_COMPANY_PURE_PLAY
        url_transactions = config.llm_service.EVALUATE_COMPANY_TRANSACTIONS

        evaluated_companies_collection = database["evaluated_companies"]

        async with httpx.AsyncClient(timeout=config.MAX_TIMEOUT) as client:
            try:
                pure_play_reasoning = await LLMService.fetch_evaluation_response(client,
                                                                                 request,
                                                                                 url_pure_play,
                                                                                 scraped_data)

                if pure_play_reasoning["pure_play"] == True:        # Can be simplified, but condition seems to fail that way.
                    await evaluated_companies_collection.insert_one(pure_play_reasoning)
                    evaluated_data = pure_play_reasoning

                else:
                    company_transactions = await CompanyService.get_company_transactions(company_request.company_name)

                    evaluated_transactions = await LLMService.fetch_evaluation_response(client,
                                                                                        request,
                                                                                        url_transactions,
                                                                                        company_transactions)

                    evaluated_data = {**pure_play_reasoning, **evaluated_transactions}
                    inserted_company = await evaluated_companies_collection.insert_one(evaluated_data)
                    evaluated_data["id"] = str(inserted_company.inserted_id)

                return EvaluatedCompanyDTO(**evaluated_data)

            except asyncio.CancelledError as e:
                raise HTTPException(status_code=499, detail="Evaluation request was cancelled.")

            except httpx.HTTPStatusError as e:

                raise HTTPException(status_code=e.response.status_code,
                                    detail=f"LLM Service returned an unexpected error: {e}")

            except httpx.TimeoutException as e:

                raise HTTPException(status_code=500,
                                    detail=f"Couldn't receive response from LLM Service on time.")

            except Exception as e:

                raise HTTPException(status_code=500,
                                    detail="An unexpected error occurred trying to reach the LLM Service. "
                                           "Please try again later.")

    @staticmethod
    async def fetch_evaluation_response(client: httpx.AsyncClient,
                                        request: Request,
                                        url: str,
                                        payload: dict) -> dict:

        task = asyncio.create_task(client.post(url, json=payload))

        while not task.done():
            if await request.is_disconnected():
                task.cancel()
                raise HTTPException(status_code=499, detail="Client disconnected during request.")

            await asyncio.sleep(0.1)

        response = await task
        response.raise_for_status()
        return response.json()
