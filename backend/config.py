from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "ai_equity_assistant"
    
    # API
    api_title: str = "AI Equity Assistant API"
    api_version: str = "1.0.0"
    api_port: int = 8000
    
    # LLM - Google Gemini
    google_api_key: Optional[str] = None
    google_model: str = "gemini-1.5-flash"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
