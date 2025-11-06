# Environment Variables Reference

This document defines all environment variables used in the project and serves as a template.

## Docker Setup (Recommended)

### Creating .env File

Copy this section to create your `.env` file in the project root:

```env
# Docker Environment Variables
# All values have defaults, .env is optional for development

# Backend Security (Optional for dev, REQUIRED for production)
# SECRET_KEY=your-secret-key-here-change-this

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
# Optional: Generate a secure SECRET_KEY for production
python -c "import secrets; print(secrets.token_urlsafe(32))"

# For development, .env file is optional - all values have defaults
```

**Notes:**
- Docker Compose automatically loads `.env` from the root directory
- All values have defaults - **.env is optional for development**
- **SECRET_KEY**: Has a default dev value; set custom value for production
- Change ports if 3000 or 8000 are already in use
- After changing values, rebuild: `docker-compose build --no-cache && docker-compose up -d`

## Manual Setup (Without Docker)

### Backend .env (place in `/backend/` folder)
```env
# Optional for dev - has default value
# For production: python -c "import secrets; print(secrets.token_urlsafe(32))"
# SECRET_KEY=your-secret-key-here-change-this
# .env
OPENAI_API_KEY=KEY_HERE
BACKEND_PORT=8000
BACK_END_URL=http://localhost:8000
FRONT_END_URL=http://localhost:3000
COMPOSE_PROJECT_NAME=synapsesquad
SECRET_KEY=SECRET_KEY_HERE
BACKEND_PORT=8000
```

### Frontend .env (place in `/frontend/` folder)
```env
REACT_APP_BACK_END_URL=http://localhost:8000
PORT=3000
```

**Note:** React only exposes variables prefixed with `REACT_APP_` at build time.

## Variable Descriptions

| Variable | Default | Purpose | Used By |
|----------|---------|---------|---------|
| `SECRET_KEY` | dev-secret-key... | Cryptographic key for JWT signing (change for production) | Backend |
| `BACKEND_PORT` | 8000 | Port for FastAPI server | Backend |
| `BACK_END_URL` | http://localhost:8000 | Backend API URL | Frontend (build time) |
| `FRONT_END_URL` | http://localhost:3000 | Frontend URL for CORS | Backend |
| `REACT_APP_BACK_END_URL` | http://localhost:8000 | Backend API URL | Frontend (manual setup) |
| `COMPOSE_PROJECT_NAME` | synapseSquad | Docker project name | Docker Compose |

## Production Notes

For production deployment:

**1. Generate a strong SECRET_KEY:**
```bash
# Generate a cryptographically secure key (DO NOT use the example below)
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**2. Update URLs to actual domain names:**
```env
# CRITICAL: Use a unique, randomly generated key for each environment
SECRET_KEY=<output-from-command-above>

BACKEND_PORT=8000
BACK_END_URL=https://api.yourcompany.com
FRONT_END_URL=https://app.yourcompany.com
```

**Security Best Practices:**
- Generate a **different** SECRET_KEY for each environment (dev/staging/production)
- **Never commit** SECRET_KEY to version control
- Minimum 32 characters, use cryptographically random values
- Store in secure secrets management system (Azure Key Vault, AWS Secrets Manager, etc.)
- Rotate keys periodically (invalidates existing JWT tokens)