import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # OpenAI API Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo"
    
    # Database Configuration
    database_url: str = "sqlite:///health_system.db"
    
    # Security Configuration
    secret_key: str = "your-secret-key-here"
    
    # Application Configuration
    debug: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
