from fastapi import Request, HTTPException
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from ...config import settings
import time
from collections import defaultdict

# Rate limiting
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit = settings.rate_limit_per_minute
        self.window = 60  # 1 minute window
        self.requests = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        
        # Clean old requests
        self.requests[client_ip] = [req_time for req_time in self.requests[client_ip] 
                                  if now - req_time < self.window]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.rate_limit:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Maximum {self.rate_limit} requests per minute."
            )
        
        # Add current request
        self.requests[client_ip].append(now)
        
        return await call_next(request)

# API Key validation
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(request: Request):
    if not settings.api_key:
        return  # Skip validation if no API key is set
        
    api_key = await api_key_header(request)
    if not api_key or api_key != settings.api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )
