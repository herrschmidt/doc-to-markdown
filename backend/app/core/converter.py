from pathlib import Path
from typing import List, Optional
from io import BytesIO
import mimetypes
import magic
from fastapi import HTTPException, UploadFile
from docling.document_converter import DocumentConverter as DoclingConverter
from docling.datamodel.base_models import InputFormat
from docling_core.types.doc.labels import GroupLabel, DocItemLabel
from docling.document_converter import (
    PdfFormatOption, WordFormatOption, ImageFormatOption,
    HTMLFormatOption, PowerpointFormatOption
)
from docling.datamodel.pipeline_options import PipelineOptions, PdfPipelineOptions
from docling.pipeline.simple_pipeline import SimplePipeline

class DocumentConverter:
    """A wrapper class for docling's DocumentConverter that handles file uploads and conversion.
    
    This class provides a high-level interface for converting various document formats to markdown.
    It supports the following formats:
    - PDF files (with OCR and table structure recognition)
    - Images (JPEG, PNG, GIF, WebP with OCR)
    - Microsoft Word documents (DOCX)
    - HTML files
    - Microsoft PowerPoint presentations (PPTX)
    
    The converter handles file type detection, validation, and cleanup automatically.
    """
    
    SUPPORTED_FORMATS = {
        'application/pdf': InputFormat.PDF,
        'image/jpeg': InputFormat.IMAGE,
        'image/png': InputFormat.IMAGE,
        'image/gif': InputFormat.IMAGE,
        'image/webp': InputFormat.IMAGE,
        'application/msword': InputFormat.DOCX,
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': InputFormat.DOCX,
        'text/html': InputFormat.HTML,
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': InputFormat.PPTX,
    }

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    def __init__(self):
        """Initialize the DocumentConverter with format-specific options.
        
        This sets up the docling converter with appropriate pipeline options for each format:
        - PDF: OCR and table structure recognition enabled
        - Images: Basic OCR enabled
        - Word: Default options
        - HTML: Default options
        - PowerPoint: Default options with SimplePipeline
        """
        # Configure PDF pipeline options
        pdf_pipeline_options = PdfPipelineOptions()
        pdf_pipeline_options.do_ocr = True  # Enable OCR for scanned documents
        pdf_pipeline_options.do_table_structure = True  # Enable table structure recognition

        # Configure base pipeline options for other formats
        base_pipeline_options = PipelineOptions()

        # Create converter with format-specific options
        self.converter = DoclingConverter(
            allowed_formats=[
                InputFormat.PDF,
                InputFormat.IMAGE,
                InputFormat.DOCX,
                InputFormat.HTML,
                InputFormat.PPTX,
            ],
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pdf_pipeline_options),
                InputFormat.IMAGE: ImageFormatOption(pipeline_options=base_pipeline_options),
                InputFormat.DOCX: WordFormatOption(pipeline_options=base_pipeline_options),
                InputFormat.HTML: HTMLFormatOption(pipeline_options=base_pipeline_options),
                InputFormat.PPTX: PowerpointFormatOption(pipeline_options=base_pipeline_options, pipeline_cls=SimplePipeline),
            }
        )

    async def detect_file_type(self, file_path: Path) -> str:
        """Detect the MIME type of a file using python-magic.
        
        Args:
            file_path (Path): Path to the file to analyze
            
        Returns:
            str: The detected MIME type (e.g., 'application/pdf', 'image/jpeg')
        """
        mime = magic.Magic(mime=True)
        return mime.from_file(str(file_path))

    def validate_file_size(self, file_size: int) -> None:
        """Validate that the file size is within acceptable limits.
        
        Args:
            file_size (int): Size of the file in bytes
            
        Raises:
            HTTPException: If the file size exceeds MAX_FILE_SIZE (413 Payload Too Large)
        """
        if file_size > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds maximum limit of {self.MAX_FILE_SIZE / 1024 / 1024}MB"
            )

    def validate_file_type(self, mime_type: str) -> None:
        """Validate that the file type is supported.
        
        Args:
            mime_type (str): MIME type to validate
            
        Raises:
            HTTPException: If the MIME type is not in SUPPORTED_FORMATS (415 Unsupported Media Type)
        """
        if mime_type not in self.SUPPORTED_FORMATS:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file type: {mime_type}"
            )

    async def convert(self, file: UploadFile, save_path: Path) -> dict:
        """Convert an uploaded file to markdown format.
        
        This method handles the complete conversion process:
        1. Reads and validates the uploaded file
        2. Saves it temporarily to disk
        3. Detects the file type
        4. Converts the file to markdown using docling
        5. Cleans up temporary files
        
        Args:
            file (UploadFile): The uploaded file from FastAPI
            save_path (Path): Path where the file should be temporarily saved
        
        Returns:
            dict: A dictionary containing:
                - content (str): The markdown content
                - metadata (dict):
                    - original_file (str): Original filename
                    - mime_type (str): Detected MIME type
                    - file_size (int): Size in bytes
        
        Raises:
            HTTPException:
                - 413 Payload Too Large: If file size exceeds MAX_FILE_SIZE
                - 415 Unsupported Media Type: If file type is not supported
                - 500 Internal Server Error: If conversion fails
        """
        try:
            # Validate file size
            file_size = 0
            contents = await file.read()
            file_size = len(contents)
            self.validate_file_size(file_size)

            # Save file temporarily to detect type
            save_path.write_bytes(contents)
            mime_type = await self.detect_file_type(save_path)
            self.validate_file_type(mime_type)

            # Convert document using the file path
            result = self.converter.convert(str(save_path))

            # Handle PowerPoint files specially
            if self.SUPPORTED_FORMATS[mime_type] == InputFormat.PPTX:
                markdown_content = ""
                for item, level in result.document.iterate_items(with_groups=True):
                    if hasattr(item, 'children'):
                        for child_ref in item.children:
                            child = child_ref.resolve(result.document)
                            if hasattr(child, 'text'):
                                markdown_content += child.text + "\n\n"
            else:
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