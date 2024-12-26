from pathlib import Path
from typing import List, Optional
import mimetypes
import magic
from fastapi import HTTPException, UploadFile
from docling.document_converter import DocumentConverter as DoclingConverter

class DocumentConverter:
    SUPPORTED_FORMATS = {
        'application/pdf': 'pdf',
        'image/jpeg': 'image',
        'image/png': 'image',
        'image/gif': 'image',
        'image/webp': 'image',
        'application/msword': 'docx',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
        'text/html': 'html',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx',
    }

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    def __init__(self):
        self.converter = DoclingConverter()

    async def detect_file_type(self, file_path: Path) -> str:
        """Detect the MIME type of a file using python-magic."""
        mime = magic.Magic(mime=True)
        return mime.from_file(str(file_path))

    def validate_file_size(self, file_size: int) -> None:
        """Validate that the file size is within acceptable limits."""
        if file_size > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds maximum limit of {self.MAX_FILE_SIZE / 1024 / 1024}MB"
            )

    def validate_file_type(self, mime_type: str) -> None:
        """Validate that the file type is supported."""
        if mime_type not in self.SUPPORTED_FORMATS:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file type: {mime_type}"
            )

    async def convert(self, file: UploadFile, save_path: Path) -> dict:
        """
        Convert an uploaded file to markdown format.
        
        Args:
            file: The uploaded file
            save_path: Path where the file should be temporarily saved
        
        Returns:
            dict: Contains markdown content and metadata
        
        Raises:
            HTTPException: If file validation fails or conversion errors occur
        """
        try:
            # Validate file size
            file_size = 0
            contents = await file.read()
            file_size = len(contents)
            self.validate_file_size(file_size)

            # Save file temporarily
            save_path.write_bytes(contents)

            # Detect and validate file type
            mime_type = await self.detect_file_type(save_path)
            self.validate_file_type(mime_type)

            # Convert document
            result = self.converter.convert(str(save_path))
            markdown_content = result.document.export_to_markdown()

            return {
                "content": markdown_content,
                "metadata": {
                    "original_file": file.filename,
                    "mime_type": mime_type,
                    "file_size": file_size,
                }
            }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error during document conversion: {str(e)}"
            )
        finally:
            # Clean up temporary file
            if save_path.exists():
                save_path.unlink()