# Frontend Documentation

## Overview
The frontend is a web application built with HTML, JavaScript, and DaisyUI that provides a user interface for converting various document formats to Markdown.

## Project Structure
```
frontend/
├── src/                      # Source code
│   ├── components/           # Reusable UI components
│   │   └── dragdrop/        # Drag and drop file upload component
│   ├── styles/              # Global styles
│   ├── utils/               # Frontend utilities
│   └── index.html           # Main HTML file
├── public/                  # Static assets
└── tests/                  # Frontend tests
```

## Development Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
cd src && python3 -m http.server 8000 --bind 0.0.0.0
```

The frontend will be available at http://0.0.0.0:8000/index.html (or your machine's IP address)

## Adding New Components
1. Create a new directory in `frontend/src/components/`
2. Include component files (JS, CSS)
3. Add documentation in the component's README.md
4. Import and use the component in other files

## Running Tests
To run frontend tests:
```bash
cd frontend && npm test
```

## Building for Production
To build the frontend for production:
```bash
cd frontend && npm run build
```