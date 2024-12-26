from pydantic import BaseModel, Field

class ConversionResponse(BaseModel):
    content: str = Field(..., description="The converted markdown content")
    metadata: dict = Field(..., description="Additional information about the conversion")

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message describing what went wrong")
