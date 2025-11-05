# Environment Variables Reference

This document defines all environment variables used in the project and serves as a template.

## Docker Setup (Recommended)

### Creating .env File

Copy this section to create your `.env` file in the project root:

```env
# Docker Environment Variables
# All values have defaults, so .env is optional

# Backend
BACKEND_PORT=8000
BACK_END_URL=http://localhost:8000

# Frontend
FRONT_END_URL=http://localhost:3000

# Docker
COMPOSE_PROJECT_NAME=synapseSquad
```

**Quick Setup:**
```bash
# Create .env file (optional - defaults work without it)
# Copy the values above into a new .env file in project root
```

**Notes:**
- Docker Compose automatically loads `.env` from the root directory
- All values have defaults (defined in docker-compose.yml), so `.env` is optional
- Change ports if 3000 or 8000 are already in use
- After changing values, run: `.\docker-rebuild.ps1`

## Manual Setup (Without Docker)

### Backend .env (place in `/backend/` folder)
```env
BACKEND_PORT=8000
FRONT_END_URL=http://localhost:3000
```

### Frontend .env (place in `/frontend/` folder)
```env
REACT_APP_BACK_END_URL=http://localhost:8000
```

**Note:** React only exposes variables prefixed with `REACT_APP_` at build time.

## Variable Descriptions

| Variable | Default | Purpose | Used By |
|----------|---------|---------|---------|
| `BACKEND_PORT` | 8000 | Port for FastAPI server | Backend |
| `BACK_END_URL` | http://localhost:8000 | Backend API URL | Frontend (build time) |
| `FRONT_END_URL` | http://localhost:3000 | Frontend URL for CORS | Backend |
| `REACT_APP_BACK_END_URL` | http://localhost:8000 | Backend API URL | Frontend (manual setup) |
| `COMPOSE_PROJECT_NAME` | synapseSquad | Docker project name | Docker Compose |

## Production Notes

For production deployment, update URLs to actual domain names:

```env
BACKEND_PORT=8000
BACK_END_URL=https://api.yourcompany.com
FRONT_END_URL=https://app.yourcompany.com
```