from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Doc-to-Markdown API"
    version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    upload_dir: str = "/tmp/doc-to-markdown"
    
    # Security settings
    api_key: str = ""  # Set this in production
    allowed_origins: list[str] = ["http://localhost:8000"]  # Add your frontend domain in production
    rate_limit_per_minute: int = 60  # Adjust based on your needs
    
    class Config:
        env_prefix = "MARKDOWN_"  # Environment variables should be prefixed with MARKDOWN_

settings = Settings()
