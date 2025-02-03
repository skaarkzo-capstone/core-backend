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
    async def evaluate_company(scraped_data: dict, company_request: CompanyRequest, request: Request) -> EvaluatedCompanyDTO:
        url_pure_play = config.llm_service.EVALUATE_COMPANY_PURE_PLAY
        url_transactions = config.llm_service.EVALUATE_COMPANY_TRANSACTIONS

        evaluated_companies_collection = database["evaluated_companies"]

        async with httpx.AsyncClient(timeout=config.MAX_TIMEOUT) as client:
            try:
                pure_play_task = asyncio.create_task(
                    client.post(url_pure_play, json=scraped_data)
                )

                while not pure_play_task.done():
                    if await request.is_disconnected():
                        pure_play_task.cancel()
                        raise HTTPException(status_code=499, detail="Client disconnected during request.")

                    await asyncio.sleep(0.1)  # Cancellation checks (non-blocking delay)

                pure_play_reasoning_response = await pure_play_task
                pure_play_reasoning_response.raise_for_status()
                pure_play_reasoning = pure_play_reasoning_response.json()

                if pure_play_reasoning.get("pure_play"):
                    await evaluated_companies_collection.insert_one(pure_play_reasoning_response.json())
                    evaluated_data = pure_play_reasoning
                else:
                    company_transactions = await CompanyService.get_company_transactions(company_request.company_name)

                    transactions_task = asyncio.create_task(
                        client.post(url_transactions, json=company_transactions)
                    )

                    while not transactions_task.done():
                        if await request.is_disconnected():
                            transactions_task.cancel()
                            raise HTTPException(status_code=499, detail="Client disconnected during request.")

                        await asyncio.sleep(0.1)  # Cancellation checks (non-blocking delay)

                    transactions_reasoning_response = await transactions_task
                    transactions_reasoning_response.raise_for_status()
                    transactions_reasoning = transactions_reasoning_response.json()

                    evaluated_data = {**pure_play_reasoning, **transactions_reasoning}

                return EvaluatedCompanyDTO(**evaluated_data.json())

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