import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Application settings
    app_name: str = "RealEstateMAS"
    version: str = "1.0.0"
    debug: bool = False
    
    # API settings
    api_base_url: Optional[str] = None
    
    # Database settings
    database_url: Optional[str] = None
    
    # External service settings
    google_maps_api_key: Optional[str] = None
    property_listing_api_key: Optional[str] = None
    
    # Logging settings
    log_level: str = "INFO"
    
    # Agent settings
    max_retries: int = 3
    timeout_seconds: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a global settings instance
settings = Settings()
