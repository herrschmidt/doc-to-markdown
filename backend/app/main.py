from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api.routes import convert

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="API for converting various document formats to markdown",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers
app.include_router(
    convert.router,
    prefix=settings.api_prefix,
    tags=["conversion"],
)

@app.get(
    "/api/health",
    tags=["health"],
    description="Check if the service is healthy",
)
async def health_check():
    return {"status": "healthy"}
