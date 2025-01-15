# Docker Setup for Magic-Markdown

This project uses Docker Compose to manage the frontend and backend services. Below are instructions for building and running the containers.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/herrschmidt/magic-markdown.git
cd magic-markdown
```

2. Create and configure your `.env` file:
```bash
cp .env.template .env
```
Edit the `.env` file with your configuration:
```env
MARKDOWN_API_KEY=your-api-key-here
MARKDOWN_BACKEND_URL=http://localhost:8001
MARKDOWN_ALLOWED_ORIGINS=http://localhost:8000
MARKDOWN_RATE_LIMIT_PER_MINUTE=60
```

3. Start the containers:
```bash
# Development mode with hot reload
docker compose -f docker/docker-compose.dev.yml up -d

# OR Production mode
docker compose -f docker/docker-compose.yml up -d
```

4. Access the application:
- Frontend: http://localhost:8000
- Backend API Docs: http://localhost:8001/docs

## Development Mode

For local development with hot reload:
```bash
docker compose -f docker/docker-compose.dev.yml up
```

This will:
- Mount local source code directories
- Enable hot reload for both frontend and backend
- Show real-time logs in the terminal

## Common Commands

### Start/Stop Services
```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v
```

### View Logs
```bash
# View all logs
docker compose logs -f

# View frontend logs
docker compose logs -f frontend

# View backend logs
docker compose logs -f backend
```

### Rebuild Containers
```bash
# Rebuild and restart
docker compose up -d --build
```

### Check Status
```bash
docker compose ps
```

## Environment Variables

The following environment variables must be set in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `MARKDOWN_API_KEY` | API key for authentication | (required) |
| `MARKDOWN_BACKEND_URL` | Backend API URL | http://localhost:8001 |
| `MARKDOWN_ALLOWED_ORIGINS` | Allowed CORS origins | http://localhost:8000 |
| `MARKDOWN_RATE_LIMIT_PER_MINUTE` | API rate limit | 60 |

## API Documentation

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## Project Structure

```
docker/
├── frontend/          # Frontend Docker configuration
│   ├── Dockerfile
│   └── entrypoint.sh
├── backend/           # Backend Docker configuration
│   ├── Dockerfile
│   └── entrypoint.sh
├── docker-compose.yml         # Production configuration
└── docker-compose.dev.yml     # Development configuration
```

## Troubleshooting

1. **Port conflicts**:
   - Frontend: 8000
   - Backend: 8001
   Ensure these ports are available

2. **Build failures**:
```bash
docker compose build --no-cache
```

3. **Container not starting**:
```bash
docker compose logs -f
```

## Citation

This project uses Docling for document conversion. If you use this software in your research, please cite:

```bibtex
@techreport{Docling,
  author = {Deep Search Team},
  month = {8},
  title = {Docling Technical Report},
  url = {https://arxiv.org/abs/2408.09869},
  eprint = {2408.09869},
  doi = {10.48550/arXiv.2408.09869},
  version = {1.0.0},
  year = {2024}
}
```

For additional help, please refer to the main project documentation.
