import pytest
import logging
from pathlib import Path
from fastapi import HTTPException, UploadFile
from app.core.converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.document_converter import (
    DocumentConverter as DoclingConverter,
    ImageFormatOption,
    PdfFormatOption,
    WordFormatOption,
    HTMLFormatOption,
    PowerpointFormatOption
)
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.datamodel.pipeline_options import PdfPipelineOptions

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture
def converter():
    """Create a DocumentConverter instance."""
    # Create a converter with default options
    converter = DocumentConverter()
    
    # Override the pipeline options to use OCR
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    
    converter.converter = DoclingConverter(
        allowed_formats=[
            InputFormat.IMAGE,
            InputFormat.PDF,
            InputFormat.DOCX,
            InputFormat.PPTX,
            InputFormat.HTML
        ],
        format_options={
            InputFormat.IMAGE: ImageFormatOption(
                pipeline_cls=StandardPdfPipeline,
                pipeline_options=pipeline_options
            ),
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options
            ),
            InputFormat.DOCX: WordFormatOption(
                pipeline_options=pipeline_options
            ),
            InputFormat.PPTX: PowerpointFormatOption(
                pipeline_options=pipeline_options,
                pipeline_cls=SimplePipeline
            ),
            InputFormat.HTML: HTMLFormatOption(
                pipeline_options=pipeline_options
            ),
        },
    )
    
    return converter

@pytest.mark.asyncio
async def test_detect_file_type(converter, sample_pdf, sample_image):
    """Test file type detection for different formats."""
    # Test PDF detection
    pdf_type = await converter.detect_file_type(sample_pdf)
    assert pdf_type == "application/pdf"

    # Test PNG detection
    png_type = await converter.detect_file_type(sample_image)
    assert png_type == "image/png"

def test_validate_file_size(converter):
    """Test file size validation."""
    # Test valid file size
    converter.validate_file_size(1024 * 1024)  # 1MB

    # Test file too large
    with pytest.raises(HTTPException) as exc_info:
        converter.validate_file_size(20 * 1024 * 1024)  # 20MB
    assert exc_info.value.status_code == 413

def test_validate_file_type(converter):
    """Test file type validation."""
    # Test valid file types
    converter.validate_file_type("application/pdf")
    converter.validate_file_type("image/jpeg")
    converter.validate_file_type("image/png")

    # Test invalid file type
    with pytest.raises(HTTPException) as exc_info:
        converter.validate_file_type("application/x-invalid")
    assert exc_info.value.status_code == 415

@pytest.mark.asyncio
async def test_convert_pdf(converter, sample_pdf, tmp_path):
    """Test PDF conversion."""
    logger.info(f"Testing PDF conversion with sample file: {sample_pdf}")
    logger.info(f"Sample PDF exists: {sample_pdf.exists()}")
    logger.info(f"Sample PDF size: {sample_pdf.stat().st_size} bytes")
    
    # Create a mock UploadFile
    class MockUploadFile(UploadFile):
        async def read(self):
            content = open(sample_pdf, "rb").read()
            logger.info(f"Read {len(content)} bytes from sample PDF")
            return content

    upload_file = MockUploadFile(
        filename="test.pdf",
        file=None,
    )

    # Test conversion
    save_path = tmp_path / "test.pdf"
    logger.info(f"Converting PDF to: {save_path}")
    result = await converter.convert(upload_file, save_path)
    
    logger.info("Conversion result metadata:")
    logger.info(f"  Original file: {result.get('metadata', {}).get('original_file')}")
    logger.info(f"  MIME type: {result.get('metadata', {}).get('mime_type')}")
    logger.info(f"  Content length: {len(result.get('content', ''))}")
    logger.info(f"  Content preview: {result.get('content', '')[:200]}")
    
    assert isinstance(result, dict)
    assert "content" in result
    assert "metadata" in result
    assert result["metadata"]["original_file"] == "test.pdf"
    assert result["metadata"]["mime_type"] == "application/pdf"

@pytest.mark.asyncio
async def test_convert_image(converter, sample_image, tmp_path):
    """Test image conversion."""
    logger.info(f"Testing image conversion with sample file: {sample_image}")
    logger.info(f"Sample image exists: {sample_image.exists()}")
    logger.info(f"Sample image size: {sample_image.stat().st_size} bytes")
    
    # Create a mock UploadFile
    class MockUploadFile(UploadFile):
        async def read(self):
            content = open(sample_image, "rb").read()
            logger.info(f"Read {len(content)} bytes from sample image")
            return content

    upload_file = MockUploadFile(
        filename="test.png",
        file=None,
    )

    # Test conversion
    save_path = tmp_path / "test.png"
    logger.info(f"Converting image to: {save_path}")
    result = await converter.convert(upload_file, save_path)
    
    logger.info("Conversion result metadata:")
    logger.info(f"  Original file: {result.get('metadata', {}).get('original_file')}")
    logger.info(f"  MIME type: {result.get('metadata', {}).get('mime_type')}")
    logger.info(f"  Content length: {len(result.get('content', ''))}")
    logger.info(f"  Content preview: {result.get('content', '')[:200]}")
    
    assert isinstance(result, dict)
    assert "content" in result
    assert "metadata" in result
    assert result["metadata"]["original_file"] == "test.png"
    assert result["metadata"]["mime_type"] == "image/png"

@pytest.mark.asyncio
async def test_convert_docx(converter, sample_docx, tmp_path):
    """Test DOCX conversion."""
    logger.info(f"Testing DOCX conversion with sample file: {sample_docx}")
    logger.info(f"Sample DOCX exists: {sample_docx.exists()}")
    logger.info(f"Sample DOCX size: {sample_docx.stat().st_size} bytes")
    
    # Create a mock UploadFile
    class MockUploadFile(UploadFile):
        async def read(self):
            content = open(sample_docx, "rb").read()
            logger.info(f"Read {len(content)} bytes from sample DOCX")
            return content

    upload_file = MockUploadFile(
        filename="test.docx",
        file=None,
    )

    # Test conversion
    save_path = tmp_path / "test.docx"
    logger.info(f"Converting DOCX to: {save_path}")
    result = await converter.convert(upload_file, save_path)
    
    logger.info("Conversion result metadata:")
    logger.info(f"  Original file: {result.get('metadata', {}).get('original_file')}")
    logger.info(f"  MIME type: {result.get('metadata', {}).get('mime_type')}")
    logger.info(f"  Content length: {len(result.get('content', ''))}")
    logger.info(f"  Content preview: {result.get('content', '')[:200]}")
    
    assert isinstance(result, dict)
    assert "content" in result
    assert "metadata" in result
    assert result["metadata"]["original_file"] == "test.docx"
    assert result["metadata"]["mime_type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    assert "Test Document" in result["content"]

@pytest.mark.asyncio
async def test_convert_pptx(converter, sample_pptx, tmp_path):
    """Test PPTX conversion."""
    logger.info(f"Testing PPTX conversion with sample file: {sample_pptx}")
    logger.info(f"Sample PPTX exists: {sample_pptx.exists()}")
    logger.info(f"Sample PPTX size: {sample_pptx.stat().st_size} bytes")
    
    # Create a mock UploadFile
    class MockUploadFile(UploadFile):
        async def read(self):
            content = open(sample_pptx, "rb").read()
            logger.info(f"Read {len(content)} bytes from sample PPTX")
            return content

    upload_file = MockUploadFile(
        filename="test.pptx",
        file=None,
    )

    # Test conversion
    save_path = tmp_path / "test.pptx"
    logger.info(f"Converting PPTX to: {save_path}")
    result = await converter.convert(upload_file, save_path)
    
    logger.info("Conversion result metadata:")
    logger.info(f"  Original file: {result.get('metadata', {}).get('original_file')}")
    logger.info(f"  MIME type: {result.get('metadata', {}).get('mime_type')}")
    logger.info(f"  Content length: {len(result.get('content', ''))}")
    logger.info(f"  Content preview: {result.get('content', '')[:200]}")
    
    assert isinstance(result, dict)
    assert "content" in result
    assert "metadata" in result
    assert result["metadata"]["original_file"] == "test.pptx"
    assert result["metadata"]["mime_type"] == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    assert "Test Presentation" in result["content"]

@pytest.mark.asyncio
async def test_convert_html(converter, sample_html, tmp_path):
    """Test HTML conversion."""
    logger.info(f"Testing HTML conversion with sample file: {sample_html}")
    logger.info(f"Sample HTML exists: {sample_html.exists()}")
    logger.info(f"Sample HTML size: {sample_html.stat().st_size} bytes")
    
    # Create a mock UploadFile
    class MockUploadFile(UploadFile):
        async def read(self):
            content = open(sample_html, "rb").read()
            logger.info(f"Read {len(content)} bytes from sample HTML")
            return content

    upload_file = MockUploadFile(
        filename="test.html",
        file=None,
    )

    # Test conversion
    save_path = tmp_path / "test.html"
    logger.info(f"Converting HTML to: {save_path}")
    result = await converter.convert(upload_file, save_path)
    
    logger.info("Conversion result metadata:")
    logger.info(f"  Original file: {result.get('metadata', {}).get('original_file')}")
    logger.info(f"  MIME type: {result.get('metadata', {}).get('mime_type')}")
    logger.info(f"  Content length: {len(result.get('content', ''))}")
    logger.info(f"  Content preview: {result.get('content', '')[:200]}")
    
    assert isinstance(result, dict)
    assert "content" in result
    assert "metadata" in result
    assert result["metadata"]["original_file"] == "test.html"
    assert result["metadata"]["mime_type"] == "text/html"
    assert "Test Document" in result["content"]

@pytest.mark.asyncio
async def test_convert_invalid_file(converter, tmp_path):
    """Test conversion with invalid file."""
    # Create a mock UploadFile with invalid content
    class MockUploadFile(UploadFile):
        async def read(self):
            return b"invalid file content"

    upload_file = MockUploadFile(
        filename="test.xyz",
        file=None,
    )

    # Test conversion failure
    with pytest.raises(HTTPException) as exc_info:
        await converter.convert(upload_file, tmp_path / "test.xyz")
    assert exc_info.value.status_code == 415
