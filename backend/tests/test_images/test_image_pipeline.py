import os
from pathlib import Path
import pytest
from PIL import Image, ImageDraw, ImageFont
from docling.datamodel.base_models import InputFormat
from docling.document_converter import (
    DocumentConverter,
    ImageFormatOption,
    PdfFormatOption,
)
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling.datamodel.pipeline_options import PdfPipelineOptions

# Create test directory if it doesn't exist
TEST_DIR = Path(__file__).parent / "samples"
TEST_DIR.mkdir(exist_ok=True)

def create_test_image(filename: str, text: str, format: str = "PNG"):
    """Create a test image with text."""
    img = Image.new('RGB', (800, 400), color='white')
    d = ImageDraw.Draw(img)
    d.text((50, 50), text, fill='black')
    path = TEST_DIR / filename
    img.save(path, format)
    return path

@pytest.fixture
def doc_converter():
    """Create a document converter with image pipeline configuration."""
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True

    return DocumentConverter(
        allowed_formats=[
            InputFormat.PDF,
            InputFormat.IMAGE,
            InputFormat.DOCX,
            InputFormat.HTML,
            InputFormat.PPTX,
        ],
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
            ),
            InputFormat.IMAGE: ImageFormatOption(
                pipeline_cls=StandardPdfPipeline
            ),
        },
    )

def test_png_conversion(doc_converter):
    """Test PNG image conversion with text."""
    test_text = "Hello, this is a PNG test image!"
    image_path = create_test_image("test.png", test_text)
    
    result = doc_converter.convert(str(image_path))
    markdown = result.document.export_to_markdown()
    
    assert test_text in markdown
    assert "![" in markdown  # Should include image reference

def test_jpeg_conversion(doc_converter):
    """Test JPEG image conversion with text."""
    test_text = "Hello, this is a JPEG test image!"
    image_path = create_test_image("test.jpg", test_text, "JPEG")
    
    result = doc_converter.convert(str(image_path))
    markdown = result.document.export_to_markdown()
    
    assert test_text in markdown
    assert "![" in markdown

def test_multiple_images(doc_converter):
    """Test converting multiple images in sequence."""
    texts = [
        "First test image",
        "Second test image",
        "Third test image"
    ]
    
    for i, text in enumerate(texts):
        image_path = create_test_image(f"test_{i}.png", text)
        result = doc_converter.convert(str(image_path))
        markdown = result.document.export_to_markdown()
        assert text in markdown

def test_image_with_complex_content(doc_converter):
    """Test image with more complex content."""
    test_text = """
    Document Title
    -------------
    This is a test document with:
    * Multiple lines
    * Different formatting
    * And bullet points
    """
    image_path = create_test_image("complex.png", test_text)
    
    result = doc_converter.convert(str(image_path))
    markdown = result.document.export_to_markdown()
    
    assert "Document Title" in markdown
    assert "bullet points" in markdown

def teardown_module(module):
    """Clean up test files after tests."""
    import shutil
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)