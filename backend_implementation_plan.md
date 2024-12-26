# Backend Implementation Plan

## Overview
Create a FastAPI backend service that uses the docling library to convert uploaded documents and images to markdown format.

## Technology Stack
- FastAPI: Web framework for building APIs
- docling: Document conversion library
- Python 3.8+ (as required by FastAPI)
- uvicorn: ASGI server

## Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── convert.py   # Document conversion endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── converter.py     # Document conversion logic
│   └── schemas/
│       ├── __init__.py
│       └── documents.py     # Pydantic models for requests/responses
└── requirements.txt
```

## API Endpoints

### 1. Document Upload and Convert
```
POST /api/v1/convert
```
- Accepts multipart/form-data with file upload
- Supports multiple file formats (PDF, MS Word, MS PowerPoint, HTML, images)
- Returns markdown content and metadata

### 2. Health Check
```
GET /api/health
```
- Returns service status

## Implementation Steps

1. **Project Setup**
   - Create backend directory structure
   - Set up virtual environment
   - Install required dependencies
   - Create requirements.txt

2. **Core Conversion Logic**
   - Implement DocumentConverter wrapper class
   - Handle different input formats
   - Implement error handling and validation
   - Add file type detection

3. **API Development**
   - Create FastAPI application
   - Implement file upload endpoint
   - Add input validation
   - Implement error handling middleware
   - Add response models
   - Add health check endpoint

4. **Testing**
   - Unit tests for converter logic
   - Integration tests for API endpoints
   - Test with different file formats
   - Performance testing for large files

5. **Documentation**
   - API documentation using FastAPI's automatic docs
   - Add usage examples
   - Document supported file formats
   - Add error codes and descriptions

## Technical Details

### Document Conversion Implementation (docling v2)
```python
from docling.document_converter import DocumentConverter, PdfFormatOption, WordFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

# Configure pipeline options
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True  # Enable OCR for scanned documents
pipeline_options.do_table_structure = True  # Enable table structure recognition

# Create converter with format-specific options
converter = DocumentConverter(
    allowed_formats=[
        InputFormat.PDF,
        InputFormat.IMAGE,
        InputFormat.DOCX,
        InputFormat.HTML,
        InputFormat.PPTX,
    ],
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
        InputFormat.DOCX: WordFormatOption(),
    }
)

# Convert document
result = converter.convert(file_path)  # Can be path or URL
markdown_content = result.document.export_to_markdown()
```

### File Upload Handling
- Use FastAPI's File upload support
- Implement file size limits
- Store uploads in temporary directory
- Clean up after conversion

### Error Handling
- Invalid file formats
- Conversion failures
- File size limits
- Malformed files
- Timeout handling

## Implementation Guidelines
- After each step, perform tests to verify the implementation
- Update this plan to mark completed steps and add any new insights
- Document any issues or deviations from the plan

## Debugging Notes
1. **docling v2 Changes**
   - Removed InputFormat and ConversionResult imports from base_models
   - Format names are now enums (InputFormat.PDF, etc.)
   - Need to configure pipeline options per format
   - OCR and table structure recognition need to be explicitly enabled
   - File conversion works better with file paths than BytesIO streams
   - Each format can have its own pipeline options and backend
   - Default pipeline options are good for most cases
   - Supports both local files and URLs

2. **API Path Changes**
   - Health check endpoint should be at `/api/health` (not `/api/v1/health`)
   - Main API prefix is already `/api/v1` in settings
   - Need to avoid double prefixing in router setup

3. **Test Files**
   - Need to create proper test files with actual content
   - PDF files need valid PDF structure (use reportlab)
   - Images need actual image data and text content (use PIL)
   - Test directory needs to be created if it doesn't exist
   - Clean up test files after each test run

4. **Dependencies**
   - Need python-magic for file type detection
   - Need reportlab for creating test PDFs
   - Need pillow for creating test images
   - Need pytest-asyncio for async tests
   - Need httpx for API testing

## Image Conversion Challenges

### Attempted Approaches
1. Using PdfFormatOption with PdfPipelineOptions for both PDF and images
   - Issue: Returns `<!-- image -->` instead of actual text
   - Tried enabling OCR but still no text extraction

2. Using TesseractCliOcrOptions with force_full_page_ocr=True
   - Issue: Tesseract fails with "Can only use .str accessor with string values!"
   - Seems to be a pandas DataFrame issue in docling's internal processing

3. Using different image formats and sizes
   - Created larger images (800x200) for better readability
   - Made text bolder by drawing it multiple times with small offsets
   - Saved with high quality (quality=100)
   - Still no text extraction

### Required Dependencies
1. Core dependencies:
   ```
   docling
   docling-core
   pypdfium2
   requests
   ```

2. OCR dependencies:
   ```
   tesseract-ocr  # System package
   tesseract-ocr-eng  # English language data
   ```

### Potential Solutions to Try
1. Use EasyOCR instead of Tesseract
   - EasyOCR is more modern and might handle images better
   - Need to install additional dependencies

2. Try different image preprocessing
   - Increase contrast
   - Add padding around text
   - Use a specific font and size

3. Try using docling's image-specific pipeline
   - Need to investigate if docling has special handling for images
   - May need to use a different format option

4. Consider using a different approach for images
   - Direct OCR without docling for images
   - Custom image processing pipeline

## References
- docling GitHub: https://github.com/DS4SD/docling
- docling Documentation: https://ds4sd.github.io/docling/
- docling v2 Changes: https://ds4sd.github.io/docling/v2/
- docling Examples: https://ds4sd.github.io/docling/examples/
- docling API Reference: https://ds4sd.github.io/docling/reference/document_converter/

## Next Steps
1. [x] Create the basic directory structure
   - Created on: 2024-12-25
   - Verified structure:
     ```
     backend/
     ├── app/
     │   ├── __init__.py
     │   ├── main.py
     │   ├── config.py
     │   ├── api/
     │   │   ├── __init__.py
     │   │   └── routes/
     │   │       ├── __init__.py
     │   │       └── convert.py
     │   ├── core/
     │   │   ├── __init__.py
     │   │   └── converter.py
     │   └── schemas/
     │       ├── __init__.py
     │       └── documents.py
     └── requirements.txt
     ```
2. [x] Set up the development environment
   - Created on: 2024-12-25
   - Installed dependencies:
     - FastAPI and related packages
     - docling library and its dependencies
   - Created basic FastAPI application
   - Tested health endpoint successfully
3. [x] Implement core conversion functionality
4. [x] Build the API endpoints
5. [x] Add tests
6. [ ] Document the API
