import logging
from functools import lru_cache

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=None,  # Disable .env file loading
        env_file_encoding="utf-8",
        extra="allow",  # This allows extra fields from environment
    )

    # App settings
    VERSION: str = Field(default="v1")
    ENV: str = Field(default="dev")
    DEBUG: bool = Field(default=False)
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = Field(default=[])

    # 60 minutes * 24 hours * 8 days = 8 days
    LOG_LEVEL: int = Field(default=logging.INFO)

    # Database settings
    POSTGRES_URL: str = Field(default="")


@lru_cache
def get_settings() -> Settings:
    """Get the settings instance."""
    return Settings()


settings = get_settings()
