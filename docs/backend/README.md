# Backend Documentation

## Overview
The backend is a FastAPI application that handles the conversion of various document formats to Markdown format.

Supported formats:
- PDF files (with OCR for scanned documents)
- Images (JPEG, PNG, GIF, WebP with OCR)
- Microsoft Word documents (DOCX)
- HTML files (with table and list preservation)
- Microsoft PowerPoint presentations (PPTX)

Features:
- Automatic file type detection
- OCR for scanned documents and images
- Table structure recognition
- List and heading preservation
- Image extraction and embedding
- File size validation (max 10MB)

## Project Structure
```
backend/
├── app/                    # Source code
│   ├── api/               # API routes
│   │   └── routes/       # Route handlers
│   ├── core/             # Core business logic
│   │   └── converter.py  # Document conversion
│   └── schemas/          # Data models
└── tests/                # Backend tests
    ├── core/             # Core tests
    ├── api/              # API tests
    └── fixtures/         # Test files
```

## Development Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start development server:
```bash
uvicorn app.main:app --reload --port 8001 --host 0.0.0.0
```

The API will be available at http://0.0.0.0:8001 (or your machine's IP address)

## Running Tests
The backend has two types of tests:
- Core tests: Test the document conversion functionality directly
- API tests: Test the REST API endpoints with file uploads

To run tests:
```bash
cd backend && pytest  # Run all tests
cd backend && pytest tests/core  # Run core tests only
cd backend && pytest tests/api   # Run API tests only
```

Test files are available in `tests/fixtures/`:
- `sample.pdf` - Sample PDF document
- `sample.png` - Sample image with text
- `sample.docx` - Sample Word document
- `sample.pptx` - Sample PowerPoint presentation
- `sample.html` - Sample HTML file

## Deployment
To deploy the backend using Docker:
```bash
cd backend && docker-compose up -d
```

## API Documentation
The API documentation is available at:
- Swagger UI: http://0.0.0.0:8001/docs
- ReDoc: http://0.0.0.0:8001/redoc