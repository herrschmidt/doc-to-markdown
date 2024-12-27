# Backend Documentation

## Overview
The backend is a FastAPI application that handles the conversion of various document formats (images, PDFs, DOC, DOCX, TXT) to Markdown format.

## Project Structure
```
backend/
├── src/                    # Source code
│   ├── api/               # API routes
│   ├── services/          # Business logic
│   ├── models/           # Data models
│   └── utils/            # Backend utilities
└── tests/                # Backend tests
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
To run backend tests:
```bash
cd backend && pytest
```

## Deployment
To deploy the backend using Docker:
```bash
cd backend && docker-compose up -d
```

## API Documentation
The API documentation is available at:
- Swagger UI: http://0.0.0.0:8001/docs
- ReDoc: http://0.0.0.0:8001/redoc