from fastapi import FastAPI
from .config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
)

@app.get(f"{settings.api_prefix}/health")
async def health_check():
    return {"status": "healthy"}
