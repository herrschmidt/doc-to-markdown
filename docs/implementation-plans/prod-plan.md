# Production Deployment Implementation Plan

This document outlines the steps and changes required to deploy the **Magic-Markdown** application in a production environment. The current setup is configured for local development, using `localhost` and ports `8000` (frontend) and `8001` (backend). For production, we need to address the following:

---

## 1. **Docker Configuration**
### Development (`docker-compose.dev.yml`)
Retain `localhost` and port bindings for local development:
```yaml
services:
  backend:
    ports:
      - "8001:8001"
  frontend:
    ports:
      - "8000:8000"
```

### Production (`docker-compose.yml`)
Remove port bindings and add a reverse proxy:
```yaml
services:
  backend:
    ports: []  # No port bindings
  frontend:
    ports: []  # No port bindings
  reverse-proxy:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/ssl/certs
    depends_on:
      - backend
      - frontend
```

---

## 2. **Deployment Options**
### Option 1: Cloudflare Tunnel (Local Development)
Use Cloudflare Tunnel to expose the local app via a subdomain.

#### Steps:
1. Install Cloudflare Tunnel:
   ```bash
   docker run -it --rm cloudflare/cloudflared:latest tunnel login
   ```

2. Create a tunnel:
   ```bash
   docker run -it --rm cloudflare/cloudflared:latest tunnel create magic-markdown
   ```

3. Configure the tunnel:
   - Add the following to `docker-compose.dev.yml`:
     ```yaml
     cloudflared:
       image: cloudflare/cloudflared:latest
       command: tunnel --hostname magic-markdown.example.com --url http://frontend:8000
       depends_on:
         - frontend
     ```

4. Start the tunnel:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

5. Access the app at `https://magic-markdown.example.com`.

---

### Option 2: VPS Deployment (Production)
Deploy the app to a VPS using Docker and a reverse proxy.

#### Steps:
1. **Provision a VPS**:
   - Choose a provider (e.g., DigitalOcean, AWS, Linode).
   - Install Docker and Docker Compose.

2. **Set up the reverse proxy**:
   - Use Nginx or Traefik for HTTPS termination and routing.
   - Update `docker-compose.yml` as shown above.

3. **Deploy the app**:
   - Copy the project to the VPS.
   - Start the app:
     ```bash
     docker-compose -f docker-compose.yml up -d
     ```

4. **Configure DNS**:
   - Point your domain (e.g., `app.example.com`) to the VPS IP.

5. **Access the app**:
   - Visit `https://app.example.com`.

---

## 3. **Environment Variables**
### Development (`.env.dev`)
Use `localhost` and default ports:
```env
MARKDOWN_API_KEY=your-secure-api-key
MARKDOWN_BACKEND_URL=http://localhost:8001
MARKDOWN_ALLOWED_ORIGINS=http://localhost:8000
MARKDOWN_RATE_LIMIT_PER_MINUTE=60
```

### Production (`.env.prod`)
Use production domain and settings:
```env
MARKDOWN_API_KEY=your-secure-api-key
MARKDOWN_BACKEND_URL=https://api.example.com
MARKDOWN_ALLOWED_ORIGINS=https://app.example.com
MARKDOWN_RATE_LIMIT_PER_MINUTE=60
```

---

## 4. **Security Enhancements**
- Use HTTPS for all communication.
- Secure the API with rate limiting and authentication.
- Use a production-ready database (if applicable).

---

## 5. **CI/CD Pipeline**
Set up a CI/CD pipeline to automate testing and deployment.

### Changes Required:
- Add a GitHub Actions workflow for production deployment:
  ```yaml
  name: Deploy to Production

  on:
    push:
      branches:
        - main

  jobs:
    deploy:
      runs-on: ubuntu-latest
      steps:
        - name: Checkout code
          uses: actions/checkout@v4

        - name: Build and push Docker images
          run: |
            docker-compose -f docker/docker-compose.yml build
            docker-compose -f docker/docker-compose.yml push

        - name: Deploy to production server
          run: |
            ssh user@production-server "cd /path/to/app && docker-compose pull && docker-compose up -d"
  ```

---

## 6. **Monitoring and Logging**
Set up monitoring and logging for the production environment.

### Changes Required:
- Add logging middleware to the backend.
- Use a monitoring tool like Prometheus and Grafana.
- Configure log rotation and storage.

---

## 7. **Testing**
Before deploying to production:
- Test the application in a staging environment.
- Verify all environment variables and configurations.

---

## 8. **Deployment Steps**
1. Update `.env` and `.env.template` with production values.
2. Configure the reverse proxy (Nginx/Traefik).
3. Build and push Docker images.
4. Deploy to the production server.
5. Test the application thoroughly.

---

## 9. **Rollback Plan**
- Maintain a backup of the previous deployment.
- Use Docker tags to roll back to a previous version if needed.

---

This updated plan reflects your requirements for separate development and production configurations, as well as options for Cloudflare Tunnel and VPS deployment. Let me know if you'd like further refinements!