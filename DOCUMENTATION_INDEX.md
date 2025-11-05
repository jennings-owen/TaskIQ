# Documentation Index

## Quick Navigation

### Getting Started
- **[README.md](README.md)** - Main project documentation
  - Three operating modes (Production, Development, Test)
  - Quick start guide
  - Testing overview
  - Troubleshooting

### Docker & Deployment
- **[DOCKER_START_GUIDE.md](DOCKER_START_GUIDE.md)** - Complete Docker usage guide
  - Production mode details
  - Development mode details
  - Test mode details
  - Common workflows
  - Troubleshooting

### Testing
- **[docs/TEST_SUITE_OVERVIEW.md](docs/TEST_SUITE_OVERVIEW.md)** - Complete test documentation
  - Test structure and organization
  - Fixture documentation
  - Test execution instructions
  - Coverage requirements
  
- **[docs/TEST_SUITE_ANALYSIS.md](docs/TEST_SUITE_ANALYSIS.md)** - Test necessity analysis
  - Rationale for each test
  - Test categorization
  - Coverage analysis

- **[docs/CICD_PIPELINE.md](docs/CICD_PIPELINE.md)** - CI/CD pipeline documentation
  - GitHub Actions workflows
  - Test automation
  - Coverage reporting
  - Artifact management

### Architecture & Design
- **[docs/PRD.md](docs/PRD.md)** - Product Requirements Document
  - Feature specifications
  - API requirements
  - Performance requirements
  - Testing requirements

- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture
  - Component design
  - Data flow
  - Technology stack

- **[docs/ADR.md](docs/ADR.md)** - Architecture Decision Records
  - Key technical decisions
  - Rationale and alternatives

### Setup & Configuration
- **[docs/SETUP.md](docs/SETUP.md)** - Manual setup instructions
  - Non-Docker installation
  - Local development setup
  - Dependency management

- **[docs/DOCKER_README.md](docs/DOCKER_README.md)** - Docker-specific setup
  - Container configuration
  - Docker Compose details

- **[docs/ENV_FORMAT.md](docs/ENV_FORMAT.md)** - Environment variables
  - Configuration reference
  - Environment setup

### Project Management
- **[docs/AGILE_PLAN.md](docs/AGILE_PLAN.md)** - Sprint plan
  - Team responsibilities
  - Sprint goals
  - Task breakdown

- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Integration guide
  - Frontend-backend integration
  - API integration patterns

## File Organization

```
Project Root/
├── README.md                      # Main documentation (START HERE)
├── DOCKER_START_GUIDE.md          # Docker usage guide
├── DOCUMENTATION_INDEX.md         # This file
├── docker-start.ps1               # Windows startup script
├── docker-start.sh                # Linux/Mac startup script
├── docker-compose.yml             # Production/Dev configuration
├── docker-compose.test.yml        # Test configuration
│
├── docs/                          # Detailed documentation
│   ├── PRD.md                     # Product requirements
│   ├── ARCHITECTURE.md            # System architecture
│   ├── ADR.md                     # Architecture decisions
│   ├── AGILE_PLAN.md              # Sprint plan
│   ├── TEST_SUITE_OVERVIEW.md     # Complete test docs
│   ├── TEST_SUITE_ANALYSIS.md     # Test analysis
│   ├── CICD_PIPELINE.md           # CI/CD documentation
│   ├── SETUP.md                   # Manual setup
│   ├── DOCKER_README.md           # Docker setup
│   └── ENV_FORMAT.md              # Environment config
│
├── backend/                       # Backend application
│   ├── main.py                    # FastAPI application
│   ├── schema.sql                 # Database schema
│   └── tests/                     # Test suite
│       ├── conftest.py            # Test fixtures
│       ├── test_tasks.py          # Task tests (36)
│       ├── test_ai.py             # AI tests (35)
│       ├── test_database.py       # Database tests (32)
│       ├── test_integration.py    # Integration tests (21)
│       └── test.db                # Test database
│
└── frontend/                      # Frontend application
    └── src/__tests__/             # Frontend tests
        ├── TaskList.test.jsx      # Component tests (20+)
        ├── TaskForm.test.jsx      # Form tests (25+)
        └── Dashboard.test.jsx     # Dashboard tests (20+)
```

## Quick Commands Reference

### Start Application
```bash
# Production (optimized, detached)
.\docker-start.ps1                 # Windows
./docker-start.sh                  # Linux/Mac

# Development (hot-reload, attached)
.\docker-start.ps1 -Dev            # Windows
./docker-start.sh -Dev             # Linux/Mac

# Test (run full test suite)
.\docker-start.ps1 -Test           # Windows
./docker-start.sh -Test            # Linux/Mac
```

### Testing
```bash
# Full test suite via Docker
.\docker-start.ps1 -Test

# View test logs
docker-compose -f docker-compose.test.yml logs backend-test
docker-compose -f docker-compose.test.yml logs frontend-test

# Cleanup
docker-compose -f docker-compose.test.yml down -v

# Manual backend tests
cd backend && pytest tests/ -v --cov=.

# Manual frontend tests
cd frontend && npm test -- --coverage
```

### Docker Management
```bash
# Stop services
docker-compose down

# Rebuild without cache
docker-compose build --no-cache

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

## Documentation Standards

### When to Update Documentation

1. **README.md** - Update for:
   - New features affecting quick start
   - Changes to operating modes
   - New troubleshooting scenarios

2. **DOCKER_START_GUIDE.md** - Update for:
   - Changes to docker-start scripts
   - New Docker configurations
   - Workflow changes

3. **docs/TEST_SUITE_OVERVIEW.md** - Update for:
   - New tests added
   - Test structure changes
   - Fixture modifications

4. **docs/CICD_PIPELINE.md** - Update for:
   - CI/CD workflow changes
   - New GitHub Actions jobs
   - Coverage requirement changes

5. **docs/PRD.md** - Update for:
   - Feature changes
   - Requirement modifications
   - API specification changes

### Documentation Principles

- Keep README.md concise with quick start focus
- Detailed information goes in docs/ directory
- Cross-reference related documents
- Update version numbers and dates
- Include code examples where helpful
- Maintain consistent formatting

## Version Information

- **Documentation Version**: 2.0
- **Last Updated**: November 5, 2025
- **Test Suite Version**: 3.0
- **PRD Version**: 1.0

## Support

For questions or issues:
1. Check relevant documentation above
2. Review troubleshooting sections in README.md
3. Check GitHub Actions logs for CI/CD issues
4. Review test logs for test failures

