from typing import Dict
from pydantic import BaseModel, Field

class ConversionMetadata(BaseModel):
    """Metadata about the converted document."""
    original_file: str = Field(..., description="Original filename of the uploaded document")
    mime_type: str = Field(..., description="Detected MIME type of the document")
    file_size: int = Field(..., description="Size of the document in bytes")

class ConversionResponse(BaseModel):
    """Response model for successful document conversion."""
    content: str = Field(
        ...,
        description="The converted markdown content",
        examples=["# Document Title\n\nThis is a paragraph.\n\n* List item 1\n* List item 2"]
    )
    metadata: ConversionMetadata = Field(
        ...,
        description="Additional information about the converted document"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "content": "# Sample Document\n\nThis is a paragraph.\n\n* List item 1\n* List item 2",
                "metadata": {
                    "original_file": "document.pdf",
                    "mime_type": "application/pdf",
                    "file_size": 12345
                }
            }
        }

class ErrorResponse(BaseModel):
    """Response model for conversion errors."""
    detail: str = Field(
        ...,
        description="Error message describing what went wrong",
        examples=[
            "File size exceeds maximum limit of 10MB",
            "Unsupported file type: application/x-binary",
            "Error during document conversion: Failed to parse PDF structure"
        ]
    )
