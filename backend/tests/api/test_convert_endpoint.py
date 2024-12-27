import pytest
from pathlib import Path
from fastapi import UploadFile
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

def test_health_check(test_client):
    """Test the health check endpoint."""
    response = test_client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_convert_pdf(test_client, sample_pdf):
    """Test PDF conversion endpoint."""
    with open(sample_pdf, "rb") as f:
        files = {"file": ("test.pdf", f, "application/pdf")}
        response = test_client.post("/api/v1/convert", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert "metadata" in data
    assert data["metadata"]["original_file"] == "test.pdf"
    assert data["metadata"]["mime_type"] == "application/pdf"

def test_convert_image(test_client, sample_image, monkeypatch):
    """Test image conversion endpoint."""
    # Override the converter's pipeline options
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    
    converter = DoclingConverter(
        allowed_formats=[InputFormat.IMAGE],
        format_options={
            InputFormat.IMAGE: ImageFormatOption(
                pipeline_cls=StandardPdfPipeline,
                pipeline_options=pipeline_options
            ),
        },
    )
    
    # Patch the converter in the app
    from app.core.converter import DocumentConverter
    def get_patched_converter():
        conv = DocumentConverter()
        conv.converter = converter
        return conv
    monkeypatch.setattr("app.api.routes.convert.DocumentConverter", get_patched_converter)
    
    # Test the endpoint
    with open(sample_image, "rb") as f:
        files = {"file": ("test.png", f, "image/png")}
        response = test_client.post("/api/v1/convert", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert "metadata" in data
    assert data["metadata"]["original_file"] == "test.png"
    assert data["metadata"]["mime_type"] == "image/png"

def test_convert_no_file(test_client):
    """Test conversion endpoint without file."""
    response = test_client.post("/api/v1/convert")
    assert response.status_code == 422  # Unprocessable Entity

def test_convert_empty_file(test_client):
    """Test conversion with empty file."""
    files = {"file": ("empty.txt", b"", "text/plain")}
    response = test_client.post("/api/v1/convert", files=files)
    assert response.status_code == 415  # Unsupported Media Type

def test_convert_large_file(test_client, tmp_path):
    """Test conversion with file exceeding size limit."""
    # Create a large file (11MB)
    large_file = tmp_path / "large.pdf"
    large_file.write_bytes(b"0" * (11 * 1024 * 1024))

    with open(large_file, "rb") as f:
        files = {"file": ("large.pdf", f, "application/pdf")}
        response = test_client.post("/api/v1/convert", files=files)
    
    assert response.status_code == 413  # Payload Too Large

def test_convert_docx(test_client, sample_docx):
    """Test DOCX conversion endpoint."""
    with open(sample_docx, "rb") as f:
        files = {"file": ("test.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        response = test_client.post("/api/v1/convert", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert "metadata" in data
    assert data["metadata"]["original_file"] == "test.docx"
    assert data["metadata"]["mime_type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    assert "Test Document" in data["content"]

def test_convert_pptx(test_client, sample_pptx):
    """Test PPTX conversion endpoint."""
    with open(sample_pptx, "rb") as f:
        files = {"file": ("test.pptx", f, "application/vnd.openxmlformats-officedocument.presentationml.presentation")}
        response = test_client.post("/api/v1/convert", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert "metadata" in data
    assert data["metadata"]["original_file"] == "test.pptx"
    assert data["metadata"]["mime_type"] == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    assert "Test Presentation" in data["content"]

def test_convert_html(test_client, sample_html):
    """Test HTML conversion endpoint."""
    with open(sample_html, "rb") as f:
        files = {"file": ("test.html", f, "text/html")}
        response = test_client.post("/api/v1/convert", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert "metadata" in data
    assert data["metadata"]["original_file"] == "test.html"
    assert data["metadata"]["mime_type"] == "text/html"
    assert "Test Document" in data["content"]

def test_convert_unsupported_type(test_client):
    """Test conversion with unsupported file type."""
    files = {"file": ("test.xyz", b"test content", "application/x-xyz")}
    response = test_client.post("/api/v1/convert", files=files)
    assert response.status_code == 415  # Unsupported Media Type
