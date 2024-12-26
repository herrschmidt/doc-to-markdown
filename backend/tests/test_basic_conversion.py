import pytest
from pathlib import Path
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from fastapi import UploadFile
from app.core.converter import DocumentConverter

def create_test_pdf(path: Path, text: str = "Test PDF Document") -> None:
    """Create a simple PDF file with some text."""
    c = canvas.Canvas(str(path))
    c.drawString(100, 750, text)
    c.save()

def create_test_image(path: Path, text: str = "Test Image") -> None:
    """Create a simple image with some text."""
    # Create a larger image with bigger text
    img = Image.new('RGB', (800, 200), color='white')
    d = ImageDraw.Draw(img)
    
    # Draw text in large size and bold
    text_x = 50
    text_y = 50
    for dx in range(3):  # Make it bolder
        for dy in range(3):
            d.text((text_x + dx, text_y + dy), text, fill='black', font=None)
    
    # Save with high quality
    img.save(path, quality=100)

@pytest.fixture
def test_files_dir():
    """Create and return the test files directory."""
    test_dir = Path(__file__).parent / "test_files"
    test_dir.mkdir(exist_ok=True)
    return test_dir

@pytest.fixture
def converter():
    """Create and return a DocumentConverter instance."""
    return DocumentConverter()

async def test_pdf_conversion(test_files_dir, converter):
    # Create a test PDF
    pdf_path = test_files_dir / "test.pdf"
    create_test_pdf(pdf_path, "Test PDF Document")
    
    # Create a mock UploadFile
    with open(pdf_path, 'rb') as f:
        content = f.read()
    
    file = UploadFile(
        filename="test.pdf",
        file=BytesIO(content)
    )
    
    # Convert the file
    result = await converter.convert(file, pdf_path)
    
    # Verify the result
    assert result["content"] is not None
    assert len(result["content"]) > 0
    assert "Test PDF Document" in result["content"]
    assert result["metadata"]["mime_type"] == "application/pdf"
    assert result["metadata"]["original_file"] == "test.pdf"
    assert result["metadata"]["file_size"] > 0

async def test_image_conversion(test_files_dir, converter):
    # Create a test image
    img_path = test_files_dir / "test.png"
    create_test_image(img_path, "Test Image")
    
    # Create a mock UploadFile
    with open(img_path, 'rb') as f:
        content = f.read()
    
    file = UploadFile(
        filename="test.png",
        file=BytesIO(content)
    )
    
    # Convert the file
    result = await converter.convert(file, img_path)
    
    # Verify the result
    assert result["content"] is not None
    assert len(result["content"]) > 0
    assert "Test Image" in result["content"]
    assert result["metadata"]["mime_type"] == "image/png"
    assert result["metadata"]["original_file"] == "test.png"
    assert result["metadata"]["file_size"] > 0