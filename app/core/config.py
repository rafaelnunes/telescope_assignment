import logging
from typing import Any, Optional, Union

from pydantic import AnyHttpUrl, Field, PostgresDsn, ValidationInfo, field_validator
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
    POSTGRES_USER: str = Field(default="")
    POSTGRES_PASSWORD: str = Field(default="")
    POSTGRES_HOST: str = Field(default="")
    POSTGRES_PORT: str = Field(default="")
    POSTGRES_DB: str = Field(default="")
    POSTGRES_URL: Union[Optional[PostgresDsn], Optional[str]] = Field(default=None)

    @field_validator("POSTGRES_URL", mode="before")
    @classmethod
    def build_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str) and len(v) > 0:
            return v

        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_HOST"),
            path=f"{values.data.get('POSTGRES_DB') or ''}",
        ).unicode_string()


settings = Settings()
