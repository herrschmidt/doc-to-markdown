import os
import pytest
import logging
from pathlib import Path
from fastapi.testclient import TestClient
from PIL import Image
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
    
    if not pdf_path.exists():
        # Create a valid PDF file with some content
        logger.info("Creating new PDF file with test content")
        c = canvas.Canvas(str(pdf_path))
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, "Test PDF Document")
        c.drawString(100, 730, "This is a test document created for testing purposes.")
        c.drawString(100, 710, "It contains some text that should be converted to markdown.")
        c.save()
        logger.info(f"PDF file created successfully, size: {pdf_path.stat().st_size} bytes")
    else:
        logger.info(f"Using existing PDF file, size: {pdf_path.stat().st_size} bytes")
    
    return pdf_path

@pytest.fixture
def sample_image(fixtures_dir):
    """Create a sample PNG image for testing."""
    img_path = fixtures_dir / "sample.png"
    logger.info(f"Creating sample PNG at: {img_path}")
    
    if not img_path.exists():
        # Create a valid PNG image with some content
        logger.info("Creating new PNG image with test content")
        img = Image.new('RGB', (200, 100), color='white')
        # Add some text to the image
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), "Test Image", fill='black')
        draw.text((10, 30), "This is a test image", fill='black')
        img.save(img_path, format='PNG')
        logger.info(f"PNG file created successfully, size: {img_path.stat().st_size} bytes")
    else:
        logger.info(f"Using existing PNG file, size: {img_path.stat().st_size} bytes")
    
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
