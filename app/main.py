from fastapi import FastAPI
from app.core.config import settings
from app.api.main import api_router
from fastapi.middleware.cors import CORSMiddleware

from app.db import check_db_connection


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.API_PREFIX)

    @app.on_event("startup")
    async def startup_event():
        await check_db_connection()

    return app


app = create_app()
