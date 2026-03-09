from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = "development"
    SECRET_KEY: str = "change-me"
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/fastapi_db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
