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

2. Configure your API key:
```bash
cp docker/docker-compose.template.yml docker/docker-compose.yml
```
Edit the `docker/docker-compose.yml` file:
- Set your API key in TWO places:
  1. Under the frontend service environment section
  2. Under the backend service environment section
- Configure the rate limit if needed (default is 60 requests/minute)

3. Start the containers:
```bash
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
| `API_KEY` | API key for authentication | (required) |
| `RATE_LIMIT` | API rate limit (requests per minute) | 60 |

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
