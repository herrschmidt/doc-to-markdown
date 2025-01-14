from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv("/workspace/magic-markdown/.env")

class Settings(BaseSettings):
    app_name: str = "Doc-to-Markdown API"
    version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    upload_dir: str = "/tmp/doc-to-markdown"
    
    # Security settings
    api_key: str  # Required, no default for security
    allowed_origins: str  # Required, no default for security
    rate_limit_per_minute: int = 60  # Default rate limit is fine to keep
    
    class Config:
        env_prefix = "MARKDOWN_"  # Environment variables should be prefixed with MARKDOWN_

settings = Settings()
