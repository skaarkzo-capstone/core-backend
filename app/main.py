from fastapi import FastAPI
from app.core.config import config
from app.api.main import api_router
from fastapi.middleware.cors import CORSMiddleware

from app.db import check_db_connection
from app.temp_company_deleting import delete_companies


def create_app() -> FastAPI:
    app = FastAPI(title=config.APP_NAME, version=config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=config.API_PREFIX)

    @app.on_event("startup")
    async def startup_event():
        await check_db_connection()
        await delete_companies()

    return app


app = create_app()
