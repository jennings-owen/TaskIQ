# Docker Start Guide

## Overview

The `docker-start` scripts provide a unified interface for running the application in three different modes: Production, Development, and Testing.

## Three Modes

### 1. Production Mode (Default - No Flags)

**Command:**
```powershell
.\docker-start.ps1          # Windows
./docker-start.sh           # Linux/Mac
```

**Features:**
- Optimized production build
- Runs in detached mode (background)
- No hot-reload
- Production-ready configuration
- Minimal resource usage

**Use When:**
- Deploying to production
- Running stable builds
- Performance testing
- Demonstrating the application

**Services:**
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

**Stop Services:**
```bash
docker-compose down
```

---

### 2. Development Mode (`-Dev` Flag)

**Command:**
```powershell
.\docker-start.ps1 -Dev     # Windows
./docker-start.sh -Dev      # Linux/Mac
```

**Features:**
- Hot-reload enabled
- Code changes reflected immediately
- Volumes mounted for live editing
- Runs in foreground (attached mode)
- Development tools enabled

**Use When:**
- Active development
- Making code changes
- Testing features locally
- Debugging

**Services:**
- Backend: http://localhost:8000 (with auto-reload)
- Frontend: http://localhost:3000 (with hot module replacement)

**Stop Services:**
- Press `Ctrl+C` (automatically runs `docker-compose down`)

---

### 3. Test Mode (`-Test` Flag)

**Command:**
```powershell
.\docker-start.ps1 -Test    # Windows
./docker-start.sh -Test     # Linux/Mac
```

**Features:**
- Runs full test suite (192+ tests)
- Backend: 127+ tests with coverage
- Frontend: 65+ tests
- Auto-generates test.db if missing
- Exits when tests complete
- Shows helpful cleanup commands

**Use When:**
- Running tests before committing
- Verifying changes don't break tests
- Checking test coverage
- CI/CD pipeline testing

**Test Breakdown:**
- `test_tasks.py`: 36 tests (CRUD operations)
- `test_ai.py`: 35 tests (AI endpoints)
- `test_database.py`: 32 tests (Database constraints)
- `test_integration.py`: 21 tests (Integration workflows)
- Frontend tests: 65+ tests (Components, forms, dashboard)

**After Tests:**
```bash
# View logs
docker-compose -f docker-compose.test.yml logs backend-test
docker-compose -f docker-compose.test.yml logs frontend-test

# Cleanup
docker-compose -f docker-compose.test.yml down -v
```

---

## Quick Reference Table

| Mode | Command | Hot-Reload | Detached | Use Case |
|------|---------|------------|----------|----------|
| **Production** | `.\docker-start.ps1` | No | Yes | Deployment, demos |
| **Development** | `.\docker-start.ps1 -Dev` | Yes | No | Active coding |
| **Testing** | `.\docker-start.ps1 -Test` | N/A | N/A | Run test suite |

## Common Workflows

### Daily Development Workflow
```powershell
# Start development environment
.\docker-start.ps1 -Dev

# Make code changes (hot-reload active)
# Test in browser: http://localhost:3000

# Stop when done (Ctrl+C)
```

### Before Committing
```powershell
# Run tests
.\docker-start.ps1 -Test

# If tests pass, commit changes
git add .
git commit -m "Your message"
git push
```

### Production Deployment
```powershell
# Start production build
.\docker-start.ps1

# Verify services are running
docker-compose ps

# View logs if needed
docker-compose logs -f

# Stop when needed
docker-compose down
```

## Troubleshooting

### Port Already in Use
```bash
# Stop all containers
docker-compose down

# Check for running containers
docker ps

# Force remove if needed
docker-compose down -v
```

### Tests Failing
```bash
# View detailed test logs
docker-compose -f docker-compose.test.yml logs backend-test

# Rebuild test images
docker-compose -f docker-compose.test.yml build --no-cache

# Check test database
ls backend/tests/test.db
```

### Development Hot-Reload Not Working
```bash
# Stop services
Ctrl+C

# Rebuild with no cache
docker-compose build --no-cache

# Restart development mode
.\docker-start.ps1 -Dev
```

## Environment Variables

Create a `.env` file in the project root to customize:

```env
# Backend
BACKEND_PORT=8000
FRONT_END_URL=http://localhost:3000

# Frontend
REACT_APP_BACK_END_URL=http://localhost:8000
```

## Additional Resources

- [README.md](README.md) - Main project documentation with quick start
- [docs/TEST_SUITE_OVERVIEW.md](docs/TEST_SUITE_OVERVIEW.md) - Complete test documentation
- [docs/CICD_PIPELINE.md](docs/CICD_PIPELINE.md) - CI/CD pipeline details
- [docker-compose.yml](docker-compose.yml) - Production/Dev configuration
- [docker-compose.test.yml](docker-compose.test.yml) - Test configuration

