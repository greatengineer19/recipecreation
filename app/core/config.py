from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = "development"
    SECRET_KEY: str = "change-me"
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/fastapi_db"
    # Optional override — set this in Railway to avoid conflicts with
    # Railway's auto-injected DATABASE_URL from its own Postgres plugin.
    NEON_DATABASE_URL: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def db_url(self) -> str:
        """Returns NEON_DATABASE_URL if set, otherwise falls back to DATABASE_URL."""
        return self.NEON_DATABASE_URL or self.DATABASE_URL


settings = Settings()
