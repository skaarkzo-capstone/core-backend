from httpx import Timeout
from pydantic_settings import BaseSettings


class Configuration(BaseSettings):
    APP_NAME: str = "SustAIn Core Backend"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/main"

    MONGO_USER: str = "localhost-root"
    MONGO_PASSWORD: str = "localhost-password"
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_DB: str = "sustain-db"

    @property
    def database_url(self):
        return (f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@"
                f"{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}?authSource=admin")

    # TODO: Add a non-None timeout when data scraper handles ending process on no response received.
    # Max timeout before endpoint returns a 500 internal service error for timing out.
    MAX_TIMEOUT: Timeout = Timeout(None)

    class DataScraperServiceConfig:
        SCRAPE_COMPANY: str = "http://localhost:8001/api/scraper/company"  # POST

    @property
    def data_scraper_service(self):
        return self.DataScraperServiceConfig()

    class LLMServiceConfig:
        LLM_BASE_URL: str = "https://da6f-67-71-45-138.ngrok-free.app"
        EVALUATE_COMPANY: str = f"{LLM_BASE_URL}/api/llm/chat"

    @property
    def llm_service(self):
        return self.LLMServiceConfig()


config = Configuration()
