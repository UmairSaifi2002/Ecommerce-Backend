from functools import lru_cache
from typing import Literal

# from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables / .env file.

    Pydantic-settings automatically:
    - reads .env file
    - maps UPPERCASE env vars to lowercase fields
    - validates types
    - raises error if required field missing
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Environment
    ENV: Literal["dev", "staging", "prod"] = "dev"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRE_MINUTES: int = 60

    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_CONNECT_CLIENT_ID: str = ""

    # Platform rules
    PLATFORM_COMMISSION_PCT: float = 15.0
    ULTRA_DISCOUNT_PCT: float = 10.0
    PRO_DISCOUNT_PCT: float = 20.0

    @property
    def is_dev(self) -> bool:
        return self.ENV == "dev"


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    lru_cache ensures .env is read only once per process,
    not on every request.
    """
    return Settings()


settings = get_settings()
