from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Read once at startup: environment variables > .env file > defaults."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Users & Items API"
    debug: bool = False
    database_url: PostgresDsn = PostgresDsn("postgresql+asyncpg://app:app@localhost:5432/app")


settings = Settings()
