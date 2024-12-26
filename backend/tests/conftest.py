import os
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def fixtures_dir():
    """Get the path to the test fixtures directory."""
    return Path(__file__).parent / "fixtures"

@pytest.fixture
def sample_pdf(fixtures_dir):
    """Create a sample PDF file for testing."""
    pdf_path = fixtures_dir / "sample.pdf"
    if not pdf_path.exists():
        # Create a minimal PDF file for testing
        with open(pdf_path, "wb") as f:
            f.write(b"%PDF-1.4\n%EOF\n")
    return pdf_path

@pytest.fixture
def sample_image(fixtures_dir):
    """Create a sample PNG image for testing."""
    img_path = fixtures_dir / "sample.png"
    if not img_path.exists():
        # Create a minimal PNG file for testing
        with open(img_path, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n\0\0\0\rIHDR\0\0\0\1\0\0\0\1\1\0\0\0\x37\x6e\xf9\x24\0\0\0\nIDAT\x08\x99c`\0\0\0\2\0\1\xe5\x27\xde\xfc\0\0\0\0IEND\xaeB`\x82")
    return img_path

@pytest.fixture
def cleanup_fixtures(fixtures_dir):
    """Clean up test files after tests."""
    yield
    # Clean up any test files
    for file in fixtures_dir.glob("*"):
        if file.is_file():
            file.unlink()
