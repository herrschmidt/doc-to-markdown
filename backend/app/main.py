from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api.routes import convert
from .api.middleware.security import RateLimitMiddleware, verify_api_key

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="""
    API for converting various document formats to markdown.
    
    This service provides a simple way to convert documents from different formats
    to markdown while preserving their structure and content. It supports:
    
    * PDF files (with OCR for scanned documents)
    * Images (JPEG, PNG, GIF, WebP with OCR)
    * Microsoft Word documents (DOC, DOCX)
    * HTML files (with table and list preservation)
    * Microsoft PowerPoint presentations (PPTX)
    
    Features:
    * Automatic file type detection
    * OCR for scanned documents and images
    * Table structure recognition
    * List and heading preservation
    * Image extraction and embedding
    * File size validation (max 10MB)
    
    The API is designed to be simple to use with a single endpoint for conversion
    and a health check endpoint for monitoring.
    """,
    contact={
        "name": "OpenHands Team",
        "email": "openhands@all-hands.dev",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],  # Restrict to needed methods
    allow_headers=["*"],
)

# Add security middleware
app.add_middleware(RateLimitMiddleware)

# Add routers with API key dependency
app.include_router(
    convert.router,
    prefix=settings.api_prefix,
    tags=["conversion"],
    dependencies=[Depends(verify_api_key)]
)

@app.get(
    "/api/health",
    tags=["health"],
    summary="Health Check",
    description="Check if the service is healthy and ready to accept requests",
    response_description="Service health status",
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {"status": "healthy"}
                }
            }
        }
    }
)
async def health_check():
    """Check the health status of the service.
    
    This endpoint can be used by monitoring tools to verify that:
    - The service is running and responding to requests
    - The web server is properly configured
    - The API routes are accessible
    
    Returns:
        dict: A simple status message indicating the service is healthy
    """
    return {"status": "healthy"}
