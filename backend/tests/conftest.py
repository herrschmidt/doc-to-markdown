import os
import pytest
import logging
from pathlib import Path
from fastapi.testclient import TestClient
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from io import BytesIO
from app.main import app

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def fixtures_dir():
    """Get the path to the test fixtures directory."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    fixtures_dir.mkdir(exist_ok=True)
    return fixtures_dir

@pytest.fixture
def sample_pdf(fixtures_dir):
    """Create a sample PDF file for testing."""
    pdf_path = fixtures_dir / "sample.pdf"
    logger.info(f"Creating sample PDF at: {pdf_path}")
    
    # Always create a new PDF file to ensure it's valid
    logger.info("Creating new PDF file with test content")
    c = canvas.Canvas(str(pdf_path))
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Test PDF Document")
    c.drawString(100, 730, "This is a test document created for testing purposes.")
    c.drawString(100, 710, "It contains some text that should be converted to markdown.")
    c.save()
    logger.info(f"PDF file created successfully, size: {pdf_path.stat().st_size} bytes")
    
    return pdf_path

@pytest.fixture
def sample_image(fixtures_dir):
    """Create a sample PNG image for testing."""
    img_path = fixtures_dir / "sample.png"
    logger.info(f"Creating sample PNG at: {img_path}")
    
    # Always create a new PNG file to ensure it's valid
    logger.info("Creating new PNG image with test content")
    img = Image.new('RGB', (1200, 800), color='white')
    d = ImageDraw.Draw(img)
    
    # Try to use a system font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    text = [
        ("Sample Document", font, 50),
        ("", small_font, 120),
        ("This is a test image with multiple lines of text.", small_font, 180),
        ("It includes:", small_font, 240),
        ("• A title", small_font, 300),
        ("• Multiple paragraphs", small_font, 360),
        ("• And bullet points", small_font, 420),
        ("", small_font, 480),
        ("Let's see how well the OCR works!", small_font, 540)
    ]
    
    for line, font_to_use, y_pos in text:
        d.text((50, y_pos), line, fill='black', font=font_to_use)
    
    img.save(img_path, format='PNG')
    logger.info(f"PNG file created successfully, size: {img_path.stat().st_size} bytes")
    
    return img_path

@pytest.fixture
def cleanup_fixtures(fixtures_dir):
    """Clean up test files after tests (disabled for debugging)."""
    yield
    # Cleanup disabled to allow inspection of test files
    logger.info(f"Test files available in: {fixtures_dir}")
    for file in fixtures_dir.glob("*"):
        if file.is_file():
            logger.info(f"  {file.name}: {file.stat().st_size} bytes")
