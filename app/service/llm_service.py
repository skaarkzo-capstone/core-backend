import httpx
from fastapi import HTTPException

from app.model.dto.company_evaluated_dto import EvaluatedCompanyDTO
from app.core.config import config
from app.db import database


class LLMService:

    @staticmethod
    async def evaluate_company(scraped_data: dict) -> EvaluatedCompanyDTO:
        url = config.llm_service.EVALUATE_COMPANY
        evaluated_companies_collection = database["evaluated_companies"]

        async with httpx.AsyncClient(timeout=config.MAX_TIMEOUT) as client:
            try:

                response = await client.post(url, json=scraped_data)
                response.raise_for_status()

                evaluated_data = response.json()
                
                evaluated_data['compliance'] = evaluated_data['score'] >= 5

                await evaluated_companies_collection.insert_one(evaluated_data)
                return EvaluatedCompanyDTO(**evaluated_data)

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
