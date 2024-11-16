from fastapi import APIRouter
from app.api.main.controller import search_controller
from app.api.main.controller import company_controller

api_router = APIRouter()
api_router.include_router(search_controller.router, prefix="/search", tags=["search"])
api_router.include_router(company_controller.router)
