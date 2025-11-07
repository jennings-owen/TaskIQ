# Agile TaskIQ - AI-Assisted Task Management System

**An intelligent task management application to support Agile teams in task planning and management.Built as part of the AI-Enabled Software Engineering Upskilling Course**

---

## Capstone Project Overview

This project showcases **Generative AI integration at every phase of the SDLC**, from requirements gathering to deployment. Built as the final capstone for the AI-Driven Software Engineering Program, it demonstrates how AI can accelerate development while maintaining production-quality standards.

---

## Quick Start

### Prerequisites -- Docker

**Required Software:**
- Docker Desktop 20.10+ ([Download](https://www.docker.com/products/docker-desktop))
- Docker Compose 2.0+ (included with Docker Desktop)

**Verify Installation:**
```bash
docker --version
docker compose version
```

### Three Operating Modes

**1. Production Mode (Default)**
```powershell
.\docker-start.ps1          # Windows
./docker-start.sh           # Linux/Mac
```
- Multi-stage optimized build with nginx
- Runs in detached mode (background)
- Production-ready configuration

**2. Development Mode**
```powershell
.\docker-start.ps1 -Dev     # Windows
./docker-start.sh -Dev      # Linux/Mac
```
- Hot-reload enabled for both frontend and backend
- Code changes reflected immediately
- Volumes mounted for live editing

**3. Test Mode**
```powershell
.\docker-start.ps1 -Test    # Windows
./docker-start.sh -Test     # Linux/Mac
```
- Runs full test suite
- Generates coverage reports
- Auto-cleanup after completion

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)

### Docker Architecture

**Multi-Stage Production Build:**
- **Frontend**: node:22-alpine (builder) → nginx:alpine (runtime)
- **Backend**: python:3.11-slim with uvicorn
- **Network**: Bridge network for inter-container communication
- **Security**: Non-root users, health checks, minimal attack surface

**Corporate Environment Support:**
- SSL certificate validation disabled for proxy/firewall compatibility
- Configurable via environment variables
- See [docs/DOCKER_README.md](docs/DOCKER_README.md) for CA certificate setup

### Environment Setup

See [ENV_FORMAT.md](docs/ENV_FORMAT.md) for complete environment variable documentation.

### Documentation

See [PRD.md](docs/PRD.md) for a complete product requirements document for this project. This includes AI-generated user stories, schema, and information about the project. The top of the document has a table of contents referencing important documentation.

---

## Project Goal

The primary goal of this capstone was to **build and present a working prototype of a software application, demonstrating the integration of Generative AI at every phase of the SDLC**.
