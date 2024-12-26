import pytest
from pathlib import Path
from fastapi import HTTPException, UploadFile
from app.core.converter import DocumentConverter

@pytest.fixture
def converter():
    """Create a DocumentConverter instance."""
    return DocumentConverter()

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
    # Create a mock UploadFile
    class MockUploadFile(UploadFile):
        async def read(self):
            return open(sample_pdf, "rb").read()

    upload_file = MockUploadFile(
        filename="test.pdf",
        file=None,
    )

    # Test conversion
    result = await converter.convert(upload_file, tmp_path / "test.pdf")
    
    assert isinstance(result, dict)
    assert "content" in result
    assert "metadata" in result
    assert result["metadata"]["original_file"] == "test.pdf"
    assert result["metadata"]["mime_type"] == "application/pdf"

@pytest.mark.asyncio
async def test_convert_image(converter, sample_image, tmp_path):
    """Test image conversion."""
    # Create a mock UploadFile
    class MockUploadFile(UploadFile):
        async def read(self):
            return open(sample_image, "rb").read()

    upload_file = MockUploadFile(
        filename="test.png",
        file=None,
    )

    # Test conversion
    result = await converter.convert(upload_file, tmp_path / "test.png")
    
    assert isinstance(result, dict)
    assert "content" in result
    assert "metadata" in result
    assert result["metadata"]["original_file"] == "test.png"
    assert result["metadata"]["mime_type"] == "image/png"

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
