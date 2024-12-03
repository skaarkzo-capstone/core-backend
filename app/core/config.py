from httpx import Timeout
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SustAIn Core Backend"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/main"

    SCRAPER_BASE_URL: str = "http://localhost:8001"
    LLM_BASE_URL: str = "https://05a9-70-27-123-150.ngrok-free.app"

    # TODO: Add a non-None timeout when data scraper handles ending process on no response received.
    MAX_TIMEOUT: Timeout = Timeout(None)

    MONGO_USER: str = "localhost-root"
    MONGO_PASSWORD: str = "localhost-password"
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_DB: str = "sustain-db"

    @property
    def database_url(self):
        return (f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@"
                f"{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}?authSource=admin")


settings = Settings()
