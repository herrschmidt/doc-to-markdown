# Doc-to-Markdown

A web application that converts various document formats to Markdown using FastAPI and DaisyUI.

## Features

- **Multiple Format Support**:
  - PDF files (with OCR for scanned documents)
  - Images (JPEG, PNG, GIF, WebP with OCR)
  - Microsoft Word documents (DOCX)
  - HTML files (with table and list preservation)
  - Microsoft PowerPoint presentations (PPTX)

- **User-Friendly Interface**:
  - Drag and drop file upload
  - Real-time conversion status
  - Markdown preview
  - Copy to clipboard
  - Download as .md file

- **Advanced Processing**:
  - Automatic file type detection
  - OCR for scanned documents and images
  - Table structure recognition
  - List and heading preservation
  - Image extraction and embedding
  - File size validation (max 10MB)

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/herrschmidt/doc-to-markdown.git
cd doc-to-markdown
```

2. Run the setup script:
```bash
./scripts/setup/setup_all.sh
```

3. Start the backend server:
```bash
cd backend
uvicorn app.main:app --reload --port 8001 --host 0.0.0.0
```

4. In a new terminal, start the frontend server:
```bash
cd frontend/src
python3 -m http.server 8000 --bind 0.0.0.0
```

5. Open http://localhost:8000/index.html in your browser

## Project Structure

```
doc-to-markdown/
├── frontend/                # Frontend application
│   ├── src/                # Source code
│   │   ├── components/     # UI components
│   │   ├── styles/        # Global styles
│   │   └── index.html     # Main HTML file
│   ├── public/            # Static assets
│   └── tests/            # Frontend tests
├── backend/               # Backend application
│   ├── app/              # Source code
│   │   ├── api/         # API routes
│   │   ├── core/        # Business logic
│   │   └── schemas/     # Data models
│   └── tests/           # Backend tests
├── docs/                 # Documentation
│   ├── frontend/        # Frontend docs
│   └── backend/         # Backend docs
└── scripts/             # Development scripts
    └── setup/          # Setup scripts
```

## Development

### Frontend Development
```bash
cd frontend
npm install
cd src && python3 -m http.server 8000 --bind 0.0.0.0
```

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001 --host 0.0.0.0
```

### Running Tests

Frontend tests:
```bash
cd frontend && npm test
```

Backend tests:
```bash
cd backend && pytest  # Run all tests
cd backend && pytest tests/core  # Run core tests only
cd backend && pytest tests/api   # Run API tests only
```

## API Documentation

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.