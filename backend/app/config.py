from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Doc-to-Markdown API"
    version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    upload_dir: str = "/tmp/doc-to-markdown"

settings = Settings()
