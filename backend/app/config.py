from pydantic import validator
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    app_name: str = "Doc-to-Markdown API"
    version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    upload_dir: str = "/tmp/doc-to-markdown"
    
    # Security settings
    api_key: str  # Required, no default for security
    rate_limit_per_minute: int = 60  # Default rate limit is fine to keep
    
    class Config:
        # Read from environment variables directly
        env_prefix = ""  # No prefix needed since we're using direct env vars
        case_sensitive = False

# Check for required environment variables
if not os.getenv("API_KEY"):
    raise ValueError("API_KEY environment variable is required")

settings = Settings()
