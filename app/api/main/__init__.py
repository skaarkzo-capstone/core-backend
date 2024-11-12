from fastapi import APIRouter
from app.api.main.controller import temp_controller

api_router = APIRouter()
api_router.include_router(temp_controller.router, prefix="/example", tags=["example"])
