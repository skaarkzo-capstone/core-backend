from fastapi import APIRouter
from app.api.main.controller import company_controller

api_router = APIRouter()
api_router.include_router(company_controller.router)
