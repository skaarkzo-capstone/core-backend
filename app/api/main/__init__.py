from fastapi import APIRouter
from app.api.main.controller import company_controller, evaluation_controller

api_router = APIRouter()
api_router.include_router(company_controller.router)
api_router.include_router(evaluation_controller.router)
