# Docker Setup Guide

This guide explains how to run the SynapseSquad application using Docker containers.

## Overview

The application consists of two containerized services:
- **Frontend**: React application running on port 3000
- **Backend**: FastAPI application running on port 8000

Both containers are orchestrated using Docker Compose and can be started with a single command.

## Prerequisites

### Required Software

| Software | Minimum Version | Download Link |
|----------|----------------|---------------|
| Docker Desktop | 20.10+ | https://www.docker.com/products/docker-desktop |
| Docker Compose | 2.0+ | Included with Docker Desktop |
| Node.js | 22.x | https://nodejs.org/ |

### System Requirements

- **Windows**: Windows 10/11 with WSL2 enabled
- **macOS**: macOS 10.15 or later
- **Linux**: Any modern distribution with Docker support

### Verify Installation

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker compose version

# Verify Docker is running
docker info

# Check Node.js version
node --version
```

### Install Frontend Dependencies

**Important**: Before running Docker, install npm packages locally:

```bash
cd frontend
npm install --legacy-peer-deps
cd ..
```

This installs packages to `frontend/node_modules`, which Docker will copy and use for building. This approach:
- Avoids npm install issues in Docker
- Uses your local environment's packages
- Faster builds (no network calls in Docker)
- Consistent with local development

## Quick Start

### Production Mode (Default - Optimized Build)

Uses `npm run build` with nginx for optimized performance:

```powershell
# Windows
.\docker-start.ps1

# Linux/macOS
./docker-start.sh
```

### Development Mode (Hot-Reload)

For active development with automatic code reloading:

```powershell
# Windows
.\docker-start.ps1 -Dev

# Linux/macOS
./docker-start.sh --dev
```

### Rebuilding Containers

When you need to rebuild from scratch (after changing environment variables, Dockerfiles, or dependencies):

```bash
# Force rebuild without cache
docker-compose build --no-cache
docker-compose up -d

# Or rebuild and start in one command
docker-compose up --build --force-recreate
```

**When to rebuild:**
- Changed environment variables (REACT_APP_BACK_END_URL)
- Modified Dockerfile
- Updated package.json or requirements.txt
- Frontend can't connect to backend
- Need a clean slate

### Manual Docker Compose

```bash
# Start containers
docker compose up --build -d

# View logs
docker compose logs -f

# Stop containers
docker compose down

# Stop all Docker containers (all projects)
docker stop $(docker ps -q)
```

## Configuration

### Environment Variables

The application uses environment variables from a `.env` file for configuration. Docker Compose automatically loads this file.

#### Setup

```bash
# Create .env file (optional - defaults work without it)
# See ENV_FORMAT.md for template and copy the Docker section

# Or create manually:
# nano .env  or  notepad .env
```

#### Available Variables

| Variable | Default | Description | Used By |
|----------|---------|-------------|---------|
| `BACKEND_PORT` | 8000 | Port for FastAPI server | Backend, Docker |
| `BACK_END_URL` | http://localhost:8000 | Backend API URL | Frontend (build time) |
| `FRONT_END_URL` | http://localhost:3000 | Frontend URL for CORS | Backend |
| `COMPOSE_PROJECT_NAME` | synapseSquad | Docker project name | Docker Compose |

#### How It Works

**docker-compose.yml uses variables:**
```yaml
ports:
  - "${BACKEND_PORT:-8000}:8000"  # Uses .env value or defaults to 8000
environment:
  - BACKEND_PORT=${BACKEND_PORT:-8000}
  - FRONT_END_URL=${FRONT_END_URL:-http://localhost:3000}
```

**Syntax:** `${VARIABLE:-default}`
- If `.env` exists and has `BACKEND_PORT=8080`, uses 8080
- If `.env` doesn't exist or variable is missing, uses default (8000)
- **No .env file required** - defaults work out of the box

#### Backend Environment Variables
The backend container receives:
- `BACKEND_PORT`: Port for FastAPI server (from .env or default: 8000)
- `FRONT_END_URL`: Frontend URL for CORS (from .env or default: http://localhost:3000)

#### Frontend Environment Variables
The frontend container receives at **build time**:
- `REACT_APP_BACK_END_URL`: Backend API URL (from .env `BACK_END_URL` or default: http://localhost:8000)
- `CHOKIDAR_USEPOLLING`: Enable file watching in Docker (dev mode)
- `WATCHPACK_POLLING`: Enable webpack polling for hot-reload (dev mode)

#### Customizing Ports

If ports 3000 or 8000 are in use:

```env
# In .env file
BACKEND_PORT=8080
BACK_END_URL=http://localhost:8080
FRONT_END_URL=http://localhost:3001
```

Then rebuild:
```bash
docker-compose build --no-cache
docker-compose up -d
```

## Accessing the Application

Once containers are running:

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | React application |
| Backend API | http://localhost:8000 | FastAPI endpoints |
| API Documentation | http://localhost:8000/docs | Interactive Swagger UI |
| API Redoc | http://localhost:8000/redoc | Alternative API docs |

## Docker Commands Reference

### Starting and Stopping

```bash
# Start containers (detached mode)
docker compose up -d

# Start containers with build
docker compose up --build -d

# Stop containers
docker compose down

# Stop and remove volumes
docker compose down -v

# Restart containers
docker compose restart

# Restart specific service
docker compose restart backend
docker compose restart frontend
```

### Viewing Logs

```bash
# View all logs
docker compose logs

# Follow logs (live)
docker compose logs -f

# View logs for specific service
docker compose logs backend
docker compose logs frontend

# View last 100 lines
docker compose logs --tail=100
```

### Container Management

```bash
# View running containers
docker compose ps

# View container details
docker compose ps -a

# Execute command in container
docker compose exec backend bash
docker compose exec frontend sh

# View container resource usage
docker stats
```

### Building and Images

```bash
# Build images without starting
docker compose build

# Build specific service
docker compose build backend

# Pull latest base images
docker compose pull

# Remove unused images
docker image prune

# Remove all project images
docker compose down --rmi all
```

## Development Workflow

### Hot Reload

Both containers support hot-reload for development:

1. **Backend**: Changes to Python files trigger automatic reload via uvicorn
2. **Frontend**: Changes to React files trigger automatic rebuild via react-scripts

Files are mounted as volumes, so changes on your host machine immediately reflect in containers.

### Making Code Changes

1. Edit files normally in your IDE
2. Changes are automatically detected
3. Backend reloads API server
4. Frontend rebuilds and refreshes browser

### Adding Dependencies

#### Backend (Python)
```bash
# Add package to requirements.txt
echo "new-package==1.0.0" >> requirements.txt

# Rebuild backend container
docker compose up --build -d backend
```

#### Frontend (Node.js)
```bash
# Install package in running container
docker compose exec frontend npm install new-package

# Or rebuild container
docker compose up --build -d frontend
```

## Architecture Details

### Container Structure

#### Backend Container
- **Base Image**: python:3.11-slim
- **Working Directory**: /app
- **Exposed Port**: 8000
- **User**: appuser (non-root)
- **Health Check**: GET /status every 30s
- **Build Strategy**: Installs Python packages from requirements.txt

#### Frontend Container (Production)
- **Base Image**: node:22-alpine (builder), nginx:alpine (runtime)
- **Working Directory**: /app (build), /usr/share/nginx/html (runtime)
- **Exposed Port**: 3000
- **User**: appuser (non-root)
- **Health Check**: wget localhost:3000 every 30s
- **Build Strategy**: 
  - Stage 1: Copies local node_modules and runs `npm run build`
  - Stage 2: Serves static files with nginx
  - Uses local node_modules to avoid npm install issues in Docker

#### Frontend Container (Development)
- **Base Image**: node:22-alpine
- **Working Directory**: /app
- **Exposed Port**: 3000
- **User**: appuser (non-root)
- **Build Strategy**: Copies local node_modules and runs `npm start`
- **Hot-Reload**: Enabled via volume mounts

### Network Configuration

Containers communicate via a Docker bridge network named `synapseSquad-network`:

```
Browser → Frontend Container (port 3000)
        → Backend Container (port 8000)
```

- Frontend can reach backend at `http://backend:8000` (internal DNS)
- Browser reaches both via `localhost` (port mapping)

### Volume Mounts

#### Backend Volumes
```yaml
- ./backend:/app              # Code hot-reload
- /app/__pycache__            # Prevent cache pollution
```

#### Frontend Volumes
```yaml
- ./frontend:/app             # Code hot-reload
- /app/node_modules           # Isolated dependencies
```

## Troubleshooting

### Port Conflicts

**Problem**: Port 3000 or 8000 already in use

**Solution**:
```bash
# Find process using port
# Windows
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Linux/macOS
lsof -i :3000
lsof -i :8000

# Kill process or change port in docker-compose.yml
```

### Container Won't Start

**Problem**: Container exits immediately

**Solution**:
```bash
# View container logs
docker compose logs backend
docker compose logs frontend

# Check for errors in build
docker compose up --build

# Remove volumes and rebuild
docker compose down -v
docker compose up --build
```

### Hot Reload Not Working

**Problem**: Code changes don't trigger reload

**Solution**:
```bash
# Ensure volumes are mounted correctly
docker compose ps

# Check file watching environment variables
docker compose exec frontend env | grep CHOKIDAR

# Restart containers
docker compose restart
```

### CORS Errors

**Problem**: Frontend can't reach backend

**Solution**:
1. Check `FRONT_END_URL` in backend environment
2. Verify both containers are running: `docker compose ps`
3. Check backend logs: `docker compose logs backend`
4. Ensure frontend uses correct backend URL

### Permission Errors

**Problem**: Permission denied errors in containers

**Solution**:
```bash
# Windows: Ensure WSL2 is enabled
wsl --set-default-version 2

# Linux: Check file ownership
sudo chown -R $USER:$USER .

# Rebuild containers
docker compose down
docker compose up --build
```

### Slow Performance on Windows

**Problem**: Containers run slowly

**Solution**:
1. Ensure WSL2 backend is enabled in Docker Desktop
2. Move project to WSL2 filesystem: `/home/username/projects/`
3. Increase Docker Desktop resources (Settings → Resources)

### Database/State Persistence

**Problem**: Data lost on container restart

**Solution**:
```bash
# Add named volume in docker-compose.yml
volumes:
  - db-data:/app/data

volumes:
  db-data:
```

## Production Considerations

The current Docker setup is optimized for development. For production:

### Required Changes

1. **Multi-stage Builds**: Separate build and runtime stages
2. **Frontend**: Build static files, serve with Nginx
3. **Backend**: Use Gunicorn with multiple workers
4. **Environment**: Separate production environment variables
5. **Security**: Remove development tools, scan for vulnerabilities
6. **Logging**: Configure structured logging
7. **Monitoring**: Add health checks and metrics

### Example Production Frontend Dockerfile

```dockerfile
# Build stage
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [React Production Build](https://create-react-app.dev/docs/production-build/)

## Common Issues & Solutions

### Docker Desktop Not Running

**Error**: "Docker Desktop is unable to start" or "unexpected end of JSON input"

**Solution**:
1. Quit Docker Desktop completely
2. Open Task Manager and end all Docker processes
3. Restart Docker Desktop
4. Wait for "Docker Desktop is running" message
5. Run: `docker info` to verify

### Corrupted Images

**Error**: "unable to get image" or build failures

**Solution**:
```powershell
# Clean up corrupted images
docker image prune -a -f

# Remove containers and rebuild
docker compose down -v
.\docker-start.ps1
```

### Port Already in Use

**Error**: "port is already allocated"

**Solution**:
```powershell
# Windows - find process using port
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Kill process by PID
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :3000
lsof -i :8000
kill <PID>
```

### Frontend Can't Connect to Backend

**Error**: "Failed to fetch status from the backend" or CORS errors

**Cause**: The `REACT_APP_BACK_END_URL` environment variable wasn't set during build

**Solution**:
```powershell
# Rebuild frontend with proper environment variable
docker compose down
docker compose build --no-cache frontend
docker compose up -d
```

**Verify backend URL is correct**:
- Check `docker-compose.yml` has: `REACT_APP_BACK_END_URL=http://localhost:8000`
- Backend must be accessible at that URL from your browser

### CORS Errors

**Error**: Cross-origin request blocked

**Solution**:
- Verify `FRONT_END_URL=http://localhost:3000` in backend environment
- Check backend CORS configuration in `main.py`
- Ensure both containers are running: `docker compose ps`

### Hot-Reload Not Working (Dev Mode)

**Solution**:
1. Check volume mounts: `docker compose ps`
2. Restart containers: `docker compose restart`

### Build Fails - "gid '1000' in use"

**Error**: `addgroup: gid '1000' in use` during Docker build

**Cause**: Alpine Linux base image already has a group with GID 1000

**Solution**: This has been fixed in the Dockerfiles. If you still see this error:
```bash
# Clean and rebuild
docker compose down
docker system prune -f
docker compose build --no-cache
docker compose up -d
```

The Dockerfiles now use `|| true` to ignore this error and use numeric UID/GID directly.

### Build Fails - General

**Solution**:
```powershell
# Check Docker is running
docker info

# Clean everything and rebuild
docker system prune -a --volumes -f
.\docker-start.ps1
```

## Quick Reference

### Startup Scripts

| Script | Purpose | Use When |
|--------|---------|----------|
| `.\docker-start.ps1` | Normal startup (uses cache) | Daily use, restarting containers |
| `.\docker-start.ps1 -Dev` | Development mode (hot-reload) | Active development |
| `docker-compose build --no-cache` | Force rebuild (no cache) | After config changes, fixing issues |

### Common Commands

```bash
# Start containers (production)
.\docker-start.ps1

# Start containers (development with hot-reload)
.\docker-start.ps1 -Dev

# Rebuild containers (after changes)
docker-compose build --no-cache
docker-compose up -d

# View logs (follow mode)
docker compose logs -f

# View logs for specific service
docker compose logs backend
docker compose logs frontend

# Stop containers
docker compose down

# Stop all Docker containers (all projects)
docker stop $(docker ps -q)

# Restart containers
docker compose restart

# Check container status
docker compose ps

# Access container shell
docker compose exec backend bash
docker compose exec frontend sh

# Clean up unused resources
docker system prune -f

# Clean up everything (nuclear option)
docker system prune -a --volumes -f
```

### Workflow Examples

```powershell
# First time setup
cd frontend
npm install --legacy-peer-deps
cd ..
.\docker-start.ps1

# Daily development
.\docker-start.ps1 -Dev
# ... make code changes ...
docker compose down

# After changing environment variables
docker-compose build --no-cache
docker-compose up -d

# After updating dependencies
cd frontend
npm install --legacy-peer-deps
cd ..
docker-compose build --no-cache
docker-compose up -d

# Troubleshooting connection issues
docker-compose build --no-cache
docker-compose up -d
```

## Summary

This Docker setup provides:
- **Production builds**: Optimized with `npm run build` and nginx
- **Development mode**: Hot-reload for rapid iteration
- **Single-command startup**: Easy for all team members
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Industry standard**: Follows Docker and microservices best practices

The dual-container architecture maintains separation of concerns and provides a solid foundation for both development and production deployment.

