from fastapi import APIRouter
from app.api.main.controller import search_controller

api_router = APIRouter()
api_router.include_router(search_controller.router, prefix="/search", tags=["search"])
