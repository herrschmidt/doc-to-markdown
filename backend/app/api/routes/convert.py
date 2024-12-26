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
        413: {"model": ErrorResponse, "description": "File too large"},
        415: {"model": ErrorResponse, "description": "Unsupported file type"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    description="Convert an uploaded document to markdown format",
)
async def convert_document(file: UploadFile) -> ConversionResponse:
    """
    Convert an uploaded document to markdown format.
    
    Supports the following formats:
    - PDF
    - Images (JPEG, PNG, GIF, WebP)
    - Microsoft Word (DOC, DOCX)
    - HTML
    - Microsoft PowerPoint (PPTX)
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
