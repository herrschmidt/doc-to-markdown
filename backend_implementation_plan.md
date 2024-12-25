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
GET /api/v1/health
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

### Document Conversion Implementation
```python
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat

async def convert_document(file_path: str) -> str:
    converter = DocumentConverter(
        allowed_formats=[
            InputFormat.PDF,
            InputFormat.IMAGE,
            InputFormat.DOCX,
            InputFormat.HTML,
            InputFormat.PPTX,
        ]
    )
    
    result = converter.convert(file_path)
    return result.document.export_to_markdown()
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
3. [ ] Implement core conversion functionality
4. [ ] Build the API endpoints
5. [ ] Add tests
6. [ ] Document the API