import os
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from PIL import Image
from reportlab.pdfgen import canvas
from io import BytesIO
from app.main import app

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
    if not pdf_path.exists():
        # Create a valid PDF file with some content
        c = canvas.Canvas(str(pdf_path))
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, "Test PDF Document")
        c.drawString(100, 730, "This is a test document created for testing purposes.")
        c.drawString(100, 710, "It contains some text that should be converted to markdown.")
        c.save()
    return pdf_path

@pytest.fixture
def sample_image(fixtures_dir):
    """Create a sample PNG image for testing."""
    img_path = fixtures_dir / "sample.png"
    if not img_path.exists():
        # Create a valid PNG image with some content
        img = Image.new('RGB', (200, 100), color='white')
        # Add some text to the image
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), "Test Image", fill='black')
        draw.text((10, 30), "This is a test image", fill='black')
        img.save(img_path, format='PNG')
    return img_path

@pytest.fixture
def cleanup_fixtures(fixtures_dir):
    """Clean up test files after tests."""
    yield
    # Clean up any test files
    for file in fixtures_dir.glob("*"):
        if file.is_file():
            file.unlink()
    if fixtures_dir.exists():
        fixtures_dir.rmdir()
