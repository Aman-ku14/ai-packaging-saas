"""
Application Configuration

Centralized settings management using Pydantic.
All environment variables and app settings are defined here.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "Packaging AI SaaS"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Database (Future)
    # DATABASE_URL: str = ""
    
    # AI Settings (Future)
    # OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
