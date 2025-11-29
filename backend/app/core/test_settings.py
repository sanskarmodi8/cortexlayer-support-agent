"""Test settings used during pytest to avoid loading real environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Lightweight settings for tests, replacing production secrets."""

    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./test.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    JWT_SECRET: str = "test-secret"

    OPENAI_API_KEY: str = "test"
    GROQ_API_KEY: str = "test"

    DO_SPACES_KEY: str = "test"
    DO_SPACES_SECRET: str = "test"
    DO_SPACES_BUCKET: str = "test-bucket"
    DO_SPACES_REGION: str = "test-region"

    STRIPE_SECRET_KEY: str = "test"
    STRIPE_WEBHOOK_SECRET: str = "test"

    META_WHATSAPP_TOKEN: str = "test"
    META_WHATSAPP_APP_SECRET: str = "test"
    META_WHATSAPP_PHONE_ID: str = "test"


settings = Settings()
