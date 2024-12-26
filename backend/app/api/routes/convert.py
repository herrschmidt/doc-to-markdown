import tempfile
from pathlib import Path
from fastapi import APIRouter, UploadFile, HTTPException
from ...core.converter import DocumentConverter
from ...schemas.documents import ConversionResponse, ErrorResponse

router = APIRouter()

@router.post(
    "/convert",
    response_model=ConversionResponse,
    responses={
        413: {"model": ErrorResponse, "description": "File too large (max 10MB)"},
        415: {"model": ErrorResponse, "description": "Unsupported file type"},
        500: {"model": ErrorResponse, "description": "Internal server error during conversion"},
    },
    description="Convert an uploaded document to markdown format",
    summary="Convert Document to Markdown",
    tags=["Conversion"],
)
async def convert_document(file: UploadFile) -> ConversionResponse:
    """Convert an uploaded document to markdown format.
    
    This endpoint accepts various document formats and converts them to markdown,
    preserving the document structure and content as much as possible.
    
    Supported formats:
    - PDF files (with OCR for scanned documents)
    - Images (JPEG, PNG, GIF, WebP with OCR)
    - Microsoft Word documents (DOC, DOCX)
    - HTML files (with table and list preservation)
    - Microsoft PowerPoint presentations (PPTX)
    
    Features:
    - Automatic file type detection
    - OCR for scanned documents and images
    - Table structure recognition
    - List and heading preservation
    - Image extraction and embedding
    - File size validation (max 10MB)
    
    Returns:
    - Markdown content
    - Original filename
    - Detected MIME type
    - File size
    
    Note: Speaker notes in PowerPoint presentations are not currently supported.
    """
    converter = DocumentConverter()
    
    # Create a temporary file to store the upload
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_path = Path(temp_file.name)
        try:
            result = await converter.convert(file, temp_path)
            return ConversionResponse(**result)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error during document conversion: {str(e)}"
            )
