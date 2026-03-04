"""
Application Configuration
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """

    # Application
    APP_NAME: str = "Stock Analysis Platform"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://stockuser:stockpass@localhost:5432/stock_db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # API Keys
    OPENAI_API_KEY: str = ""
    TUSHARE_TOKEN: str = ""
    ALPHA_VANTAGE_API_KEY: str = ""
    NEWS_API_KEY: str = ""

    # Security
    SECRET_KEY: str = "dev_secret_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost"]

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Cache TTL (seconds)
    CACHE_TTL_SHORT: int = 300  # 5 minutes
    CACHE_TTL_MEDIUM: int = 1800  # 30 minutes
    CACHE_TTL_LONG: int = 3600  # 1 hour

    # News
    NEWS_FETCH_INTERVAL: int = 1800  # 30 minutes
    NEWS_MAX_IMPACT_SCORE: int = 100
    NEWS_API_DAILY_LIMIT: int = 100  # NewsAPI.org free tier

    # Report Generation
    REPORT_TEMPLATES_DIR: str = "app/templates/reports"
    REPORT_OUTPUT_DIR: str = "reports"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
