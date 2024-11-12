from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SustAIn Core Backend"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/main"
    # Will add more setting (e.g., DATABASE_URL)


settings = Settings()
