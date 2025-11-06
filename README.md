# Agile TaskIQ - AI-Driven Task Management System

**An intelligent task management application demonstrating AI integration across the entire Software Development Life Cycle**

[![Tests](https://img.shields.io/badge/tests-94%20passing-brightgreen)]()
[![Coverage](https://img.shields.io/badge/coverage-80%25-yellowgreen)]()
[![Documentation](https://img.shields.io/badge/docs-comprehensive-blue)]()

---

## 🎯 Capstone Project Overview

This project showcases **Generative AI integration at every phase of the SDLC**, from requirements gathering to deployment. Built as the final capstone for the AI-Driven Software Engineering Program, it demonstrates how AI can accelerate development while maintaining production-quality standards.

### Key Features
- ✅ **AI-Powered Priority Scoring** - Automatic task prioritization based on deadline and effort
- ✅ **Agile T-Shirt Sizing** - Complexity estimation (XS, S, M, L, XL)
- ✅ **Task Dependencies** - Visual dependency tracking and management
- ✅ **JWT Authentication** - Secure user authentication with bcrypt password hashing
- ✅ **Real-time Updates** - Responsive React UI with instant feedback
- ✅ **Comprehensive Testing** - 94 passing tests with 80%+ coverage

---

## 🚀 Quick Start

### Prerequisites

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
- Runs full test suite (192+ tests)
- Generates coverage reports
- Auto-cleanup after completion

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)

### Demo Credentials
Use these pre-seeded accounts:
- Email: `alice.j@agiletaskiq.com` | Password: `password123`
- Email: `bob.smith@agiletaskiq.com` | Password: `password123`

Or register a new account via the UI.

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
**No configuration required for development!** The app works out of the box with sensible defaults.

For production deployment, set a custom `SECRET_KEY`:
```bash
# Generate a secure key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Set in environment or .env file
SECRET_KEY=<generated-key-here>
```

See [ENV_FORMAT.md](docs/ENV_FORMAT.md) for complete environment variable documentation.

### Documentation

**Getting Started:**
- **Docker Quick Start**: [DOCKER_START_GUIDE.md](DOCKER_START_GUIDE.md) - Three operating modes explained
- **Docker Setup Guide**: [docs/DOCKER_README.md](docs/DOCKER_README.md) - Complete Docker reference with troubleshooting
- **Manual Setup**: [docs/SETUP.md](docs/SETUP.md) - Non-Docker installation

**Technical Documentation:**
- **Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design with UML diagrams
- **Product Requirements**: [docs/PRD.md](docs/PRD.md) - 470+ line PRD with user stories
- **Security Review**: [docs/SECURITY_REVIEW.md](docs/SECURITY_REVIEW.md) - Security audit findings
- **ADR**: [docs/ADR.md](docs/ADR.md) - Architecture decision records

**Development & Testing:**
- **Test Suite**: [docs/TEST_SUITE_OVERVIEW.md](docs/TEST_SUITE_OVERVIEW.md) - Complete test documentation
- **CI/CD Pipeline**: [docs/CICD_PIPELINE.md](docs/CICD_PIPELINE.md) - Pipeline and testing details
- **Agile Plan**: [docs/AGILE_PLAN.md](docs/AGILE_PLAN.md) - Sprint plan and team responsibilities
- **Environment Variables**: [docs/ENV_FORMAT.md](docs/ENV_FORMAT.md) - Configuration reference

---

## 🎯 Project Goal

The primary goal of this capstone is to **build and present a working prototype of a software application, demonstrating the integration of Generative AI at every phase of the SDLC**. You will act as a full-stack developer, using AI as your co-pilot for planning, architecture, coding, testing, and documentation.

---

## ✅ Deliverables - All Complete!

All capstone requirements have been met with AI assistance throughout the SDLC.

### Documentation ✅
- ✅ **[Product Requirements Document](docs/PRD.md)** - 470+ lines with:
  - 40+ brainstormed features across 8 categories
  - 3 detailed user personas
  - 10 user stories with Given/When/Then acceptance criteria
- ✅ **[Architecture Document](docs/ARCHITECTURE.md)** - System design with:
  - Auto-generated PlantUML Component Diagram
  - Auto-generated PlantUML Sequence Diagram
  - Complete API endpoint catalog (25+ endpoints)
- ✅ **[Architecture Decision Records](docs/ADR.md)** - Technical decisions with justifications
- ✅ **[Security Review](docs/SECURITY_REVIEW.md)** - 11 security findings with remediation guidance

### Backend Application ✅
- ✅ **Complete REST API** - FastAPI with 25+ endpoints
- ✅ **[Database Schema](backend/schema.sql)** - AI-generated SQLite schema with 5 tables
- ✅ **[Unit Tests](backend/tests/)** - 94 passing tests with 80%+ coverage
- ✅ **JWT Authentication** - Secure user auth with bcrypt password hashing

### Frontend Application ✅
- ✅ **[React Frontend](frontend/)** - Full-featured UI with 15+ components
- ✅ **[Figma-to-React Components](artifacts/figma/)** - Components generated from design mockups

### AI Code ✅
- ✅ **[Jupyter Notebook](artifacts/PRD_Generator/demos/demo_notebook.ipynb)** - PRD generation demo
- ✅ **[CrewAI Agent System](artifacts/PRD_Generator/agents_custom.py)** - Multi-agent PRD generator

**Status**: 🎉 **Ready for Demo Day!**

---


---

## 💡 Suggested Project Ideas

You are encouraged to submit a project proposal for a tool of your choice. To get you started, here are some sample projects that align well with the course content:

* **AI-Powered Requirement Analyzer:** An application that takes a vague problem statement and generates a detailed PRD, user stories, and acceptance criteria.
* **Automated Test Case Assistant:** A tool that reads a Python function or API endpoint and generates a comprehensive suite of `pytest` unit tests, including edge cases.
* **CI/CD Pipeline Summarizer:** An application that ingests CI/CD logs and generates a human-readable summary of build successes, failures, and test results.
* **RAG-Powered Documentation Chatbot:** A chatbot with a RAG backend that can answer questions about a specific codebase or technical document.

---

## 🗓️ Timeline & Schedule

### **Day 9: Build Day (Focus: Implementation)**

This day is dedicated entirely to hands-on development. Follow the workflow below to build your application.

* **Morning (9:00 AM - 12:15 PM):** Project Planning, Architecture, and Backend Development.
* **Afternoon (1:15 PM - 4:30 PM):** Quality Assurance, Frontend Development, and Integration.

### **Day 10: Demo Day (Focus: Presentation & Showcase)**

* **Morning (9:00 AM - 12:00 PM): Final Preparations**
    * Finalize any remaining code and integration tasks.
    * Thoroughly test your application for the live demo.
    * Prepare your 10-15 minute presentation slides.
* **Afternoon (1:00 PM - 4:30 PM): Capstone Project Demos**
    * Each student/team will present their project to the class.
    * Celebrate your hard work and see what your peers have built!

---

## 🚀 Step-by-Step Workflow

This is your roadmap for Day 9. Use this workflow to ensure you touch on all the key skills learned during the course.

### **Phase 1: AI as Product Manager (Planning & Requirements)**

* **Goal:** Create a comprehensive PRD.
* **Action:**
    1.  Start with a high-level idea for your application.
    2.  Use an LLM to brainstorm features, user personas, and user stories with acceptance criteria (as you did on **Day 1**).
    3.  Provide the brainstormed content and a template to the LLM to generate a formal `prd.md` file.
    * **Artifact:** `prd.md`

### **Phase 2: AI as Architect (Design & Architecture)**

* **Goal:** Define your application's architecture and data structure.
* **Action:**
    1.  Feed your `prd.md` to an LLM.
    2.  Prompt it to generate a high-level system architecture. Ask for **diagrams-as-code (PlantUML)** for your architecture document (as you did on **Day 2**).
    3.  Prompt it to generate the `CREATE TABLE` statements for your database schema.
    * **Artifacts:** `architecture.md` (with diagrams), `schema.sql`

### **Phase 3: AI as Backend Developer (Coding)**

* **Goal:** Build a functional FastAPI backend.
* **Action:**
    1.  Provide your `schema.sql` to an LLM.
    2.  Prompt it to generate Pydantic and SQLAlchemy models.
    3.  Prompt it to generate the FastAPI application boilerplate with full CRUD endpoints for your models (as you did on **Day 3**).
    4.  Integrate the generated code and connect it to a live SQLite database.
    * **Artifacts:** `main.py`, `onboarding.db` (or similar)

### **Phase 4: AI as QA Engineer (Testing & Security)**

* **Goal:** Ensure your backend is robust and secure.
* **Action:**
    1.  Provide your `main.py` source code to an LLM.
    2.  Prompt it to generate a suite of `pytest` unit tests for your API, including "happy path" and edge cases (as you did on **Day 4**).
    3.  Prompt it to act as a security expert and identify potential vulnerabilities in your code (e.g., SQL injection, lack of input validation).
    * **Artifacts:** `test_main.py`, `security_review.md`

### **Phase 5: AI as Frontend Developer (UI/UX)**

* **Goal:** Create a user interface for your application.
* **Action:**
    1.  Create a simple wireframe or find a screenshot of a UI you like.
    2.  Use a **vision-capable LLM** to generate a React component with Tailwind CSS from that image (as you did on **Day 7/8**).
    3.  Prompt a text-based LLM to create additional components as needed.
    * **Artifact:** `src/App.js` and other React components.

---

## 🎤 Presentation Guidelines

Your final presentation should be a concise and engaging overview of your project. Please include the following:

1.  **Project Title & Goal:** What did you build and why?
2.  **AI-Assisted Workflow:** Showcase how you used GenAI in **at least three distinct phases** of the SDLC.
    * Show a "before" (the prompt) and "after" (the generated artifact).
3.  **Technical Architecture:** Briefly explain your system design.
4.  **Live Demo:** A walkthrough of your working application. This is the most important part!
5.  **Challenges & Learnings:** What was challenging? What were your key takeaways from the project?

---

## 🧪 Testing & Quality Assurance

### Quick Test Execution

**Run Full Test Suite (Recommended)**
```powershell
.\docker-start.ps1 -Test    # Windows
./docker-start.sh -Test     # Linux/Mac
```

This runs 192+ tests across backend and frontend:
- Backend: 127+ tests (CRUD, AI endpoints, database, integration)
- Frontend: 65+ tests (components, forms, dashboard)
- Auto-generates test.db if missing
- Generates coverage reports
- Shows helpful commands for viewing logs

**Manual Test Execution**
```bash
# Backend tests
cd backend
pytest tests/ -v --cov=. --cov-report=html

# Frontend tests
cd frontend
npm test -- --coverage

# View logs after Docker tests
docker-compose -f docker-compose.test.yml logs backend-test
docker-compose -f docker-compose.test.yml logs frontend-test

# Cleanup
docker-compose -f docker-compose.test.yml down -v
```

### Test Structure

```
backend/tests/
├── conftest.py              # Pytest fixtures (auto-generates test.db)
├── test_tasks.py            # 36 tests - CRUD operations
├── test_ai.py               # 35 tests - AI endpoints
├── test_database.py         # 32 tests - Database constraints
├── test_integration.py      # 21 tests - Integration workflows
└── test.db                  # Test database (auto-generated)

frontend/src/__tests__/
├── TaskList.test.jsx        # 20+ tests - Component tests
├── TaskForm.test.jsx        # 25+ tests - Form validation
└── Dashboard.test.jsx       # 20+ tests - Analytics display
```

### Coverage Requirements

- Backend: Minimum 80% (enforced in CI/CD)
- Frontend: Tracked (informational)
- Critical Paths: > 95%
- Performance: All API tests validate < 200ms response time

### CI/CD Integration

Tests run automatically on every push to main/master/develop:
- Uses same `docker-compose.test.yml` configuration
- Uploads coverage reports to Codecov
- Fails pipeline if tests fail or coverage < 80%
- Generates test logs as artifacts

See [Test Suite Overview](docs/TEST_SUITE_OVERVIEW.md) and [CI/CD Pipeline](docs/CICD_PIPELINE.md) for complete details.

---

## 🔒 Security

### Security Features Implemented

- ✅ **JWT Authentication** - Secure token-based authentication
- ✅ **Password Hashing** - bcrypt with SHA256 fallback
- ✅ **Input Validation** - Comprehensive Pydantic schema validation
- ✅ **SQL Injection Protection** - SQLAlchemy ORM prevents SQL injection
- ✅ **CORS Configuration** - Restricted to frontend origin
- ✅ **Environment-Based Secrets** - Configurable SECRET_KEY for production

### Security Review

Comprehensive security audit completed with 11 findings documented:
- **0 Critical** vulnerabilities
- **1 High** (SECRET_KEY - mitigated with environment variable)
- **3 Medium** (CORS, rate limiting, input validation)
- **4 Low** (best practice recommendations)
- **3 Informational** (documentation and monitoring)

See [Security Review](docs/SECURITY_REVIEW.md) for complete assessment and remediation guidance.

### Production Recommendations

For production deployment:
1. Set a unique, randomly generated `SECRET_KEY`
2. Implement rate limiting on authentication endpoints
3. Tighten CORS to production domains only
4. Enable HTTPS/TLS
5. Use secrets management (Azure Key Vault, AWS Secrets Manager)
6. Implement audit logging

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

The project includes automated CI/CD workflows:

**CI/CD Pipeline** (`.github/workflows/ci.yml`):
- Backend and frontend testing
- Code linting and quality checks
- Docker build validation
- Integration testing
- Coverage reporting

**Security Scan** (`.github/workflows/security.yml`):
- Automated security scanning
- Dependency vulnerability checks
- Secret detection
- Weekly scheduled scans

### Workflow Status

![CI/CD](https://img.shields.io/badge/CI%2FCD-passing-brightgreen)
![Security](https://img.shields.io/badge/Security-scanned-blue)
![Coverage](https://img.shields.io/badge/coverage-80%25-yellowgreen)

See [GitHub Actions README](.github/workflows/README.md) for detailed workflow documentation.

---

## 📊 Project Structure

```
220372-AG-AISOFTDEV-Team-4-SynapseSquad/
├── backend/                        # FastAPI backend application
│   ├── app/                       # Application code
│   │   ├── main.py               # FastAPI entry point
│   │   ├── auth.py               # JWT authentication
│   │   ├── tasks.py              # Task endpoints
│   │   ├── users.py              # User/auth endpoints
│   │   ├── ai.py                 # AI endpoints
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── schemas.py            # Pydantic schemas
│   │   └── database.py           # DB connection
│   ├── tests/                    # Test suite (94 tests)
│   │   ├── conftest.py          # Pytest fixtures
│   │   ├── test_tasks.py        # Task tests
│   │   ├── test_ai.py           # AI tests
│   │   ├── test_crud.py         # CRUD tests
│   │   └── test_integration.py  # Integration tests
│   ├── Dockerfile               # Backend container config
│   ├── schema.sql               # Database DDL
│   ├── seed_data.sql            # Demo data
│   └── team_synapse.db          # SQLite database
│
├── frontend/                      # React frontend application
│   ├── src/
│   │   ├── App.js               # Main component
│   │   ├── components/          # React components (15+)
│   │   ├── contexts/            # AuthContext
│   │   └── __tests__/           # Frontend tests
│   ├── Dockerfile               # Frontend container config (multi-stage)
│   ├── nginx.conf               # Nginx configuration for production
│   └── package.json
│
├── docs/                          # Comprehensive documentation
│   ├── PRD.md                   # Product Requirements (470+ lines)
│   ├── ARCHITECTURE.md          # System design with UML
│   ├── ADR.md                   # Architecture decisions
│   ├── SECURITY_REVIEW.md       # Security audit (11 findings)
│   ├── DOCKER_README.md         # Complete Docker reference
│   ├── AGILE_PLAN.md            # Sprint plan
│   ├── ENV_FORMAT.md            # Environment variables
│   ├── SETUP.md                 # Manual setup guide
│   └── TEST_SUITE_OVERVIEW.md   # Test documentation
│
├── artifacts/                     # AI-generated artifacts
│   ├── PRD_Generator/           # CrewAI multi-agent system
│   │   ├── agents_custom.py    # Agent implementation
│   │   └── demos/
│   │       └── demo_notebook.ipynb  # Jupyter demo
│   └── figma/                   # Figma-to-React components
│
├── .github/workflows/            # CI/CD automation
│   ├── ci.yml                   # Main CI/CD pipeline
│   └── security.yml             # Security scanning
│
├── DOCKER_START_GUIDE.md         # Docker quick start (3 modes)
├── docker-compose.yml            # Production/dev config
├── docker-compose.test.yml       # Test config
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🎯 Team Responsibilities

Based on [Agile Plan](docs/AGILE_PLAN.md):

| Member | Role | Responsibilities |
|--------|------|------------------|
| Member 1 (George) | Database Design | Schema design, constraints, indexes |
| Member 2 (Kristy) | Backend Development | FastAPI endpoints, business logic, database integration |
| Member 3 (Owen) | Frontend Development | React components, API integration, UI/UX |
| Member 4 (Lawrence) | Integration & Testing | Unit tests, integration tests, security review, documentation |

---

## 📝 Submission & Evaluation

* **Submission:** Please push your complete project, including all artifacts and source code, to a GitHub repository and submit the link.
* **Evaluation Criteria:** Projects will be evaluated based on:
    1.  **Completeness:** Were all required deliverables submitted?
    2.  **Functionality:** Does the application work as demonstrated?
    3.  **Innovative Use of AI:** How effectively and creatively did you leverage GenAI across the SDLC?
    4.  **Documentation Quality:** Is the PRD and architecture well-defined?
    5.  **Presentation Clarity:** Was the demo and explanation clear and professional?

---

## 💻 API Quick Reference

This document summarizes the backend HTTP API for quick handoff to frontend or training/data engineers.

### Run the server

Start the development server (from repository root):

```pwsh
uvicorn backend.app.main:app --reload
```

The SQLite DB used by the service (seeded for development) is at `backend/team_synapse.db`.

### Endpoints (summary)

- `GET /tasks` — list tasks
    - Response: array of task objects with fields: `id`, `title`, `description`, `deadline`, `estimated_duration`, `status`, `priority_score`, `tshirt_size`.

- `GET /tasks/{id}` — fetch a single task
    - 404 if not found.

- `POST /tasks` — create task
    - Required: `title` (string)
    - Optional: `description`, `deadline` (ISO 8601 or empty string), `estimated_duration` (int), `status`, `user_id` (int)
    - Behavior: if `user_id` is omitted the server will create/use a default `system@local` user and attach the task to it. If a supplied `user_id` does not exist the server returns 400.

- `PUT /tasks/{id}` — update a task
    - Accepts the same fields as POST; returns 404 if the task does not exist.

- `DELETE /tasks/{id}` — delete a task
    - Returns `{ "ok": true }` on success; 404 if not found.

- `POST /ai/rank` — rank tasks
    - Request: `{"tasks": [{"title": ..., "task_id": optional, "deadline": ..., "estimated_duration": ...}]}`
    - Query param: `?persist=true` will write computed priority scores to `task_priority_scores` (requires `task_id` to be provided and valid).

- `POST /ai/size` — general size helper (ephemeral)
    - Returns recommended size based on height/weight/gender; persistence is not supported on this endpoint.

- `POST /tasks/{task_id}/ai/size` — compute and optionally persist t-shirt size
    - Query param `?persist=true` will upsert a row into `task_tshirt_scores` for the given `task_id`.

### Example requests

- Minimal create (curl):

```pwsh
curl -X POST "http://127.0.0.1:8000/tasks" -H "Content-Type: application/json" -d '{"title":"Create landing page"}'
```

- Full create (curl):

```pwsh
curl -X POST "http://127.0.0.1:8000/tasks" -H "Content-Type: application/json" -d '{"title":"Implement login","description":"OAuth 2.0","deadline":"2025-11-20T17:00:00Z","estimated_duration":8}'
```

- Compute and persist a t-shirt size for task 1:

```pwsh
curl -X POST "http://127.0.0.1:8000/tasks/1/ai/size?persist=true" -H "Content-Type: application/json" -d '{"height_cm":170,"weight_kg":70,"gender":"male","fit_preference":"regular"}'
```

### Response examples

- A created task (POST /tasks) returns the task object with an `id`:

```
{
    "title": "smoke-test",
    "description": "smoke",
    "deadline": null,
    "estimated_duration": 2,
    "status": "pending",
    "id": 9,
    "priority_score": null,
    "tshirt_size": null
}
```

### Notes and guidance

- Validation and error codes
    - 400: client-supplied `user_id` does not exist or other client validation errors
    - 404: task not found for GET/PUT/DELETE
    - 422: Pydantic validation errors (invalid datetimes, wrong types)

- Behavior choices
    - For now the API accepts optional/blank values and coerces empty strings for `deadline` and `estimated_duration` to `null` to be forgiving to frontend forms.
    - The server currently creates/uses a default `system@local` user when `user_id` is omitted. If you plan to require authentication, make `user_id` required and return 400 when missing.

- DB and migrations
    - The project includes SQLAlchemy models. If you change models in production, add Alembic migrations. SQLite has limited ALTER support — a typical migration may require table copy/recreate.

### Running tests

Run the backend tests (fast):

```pwsh
pytest backend/tests -q
```

### Contact points

If frontend engineers need more fields, add them to Pydantic models in `backend/app/schemas.py` and the database models in `backend/app/models.py`. Coordinate schema changes with the team and add an Alembic migration.

---

## 🆘 Troubleshooting

### Backend won't start

```bash
# Check Python version (requires 3.8+)
python --version

# Install dependencies
pip install -r requirements.txt

# Check environment variables
cat .env  # Linux/macOS
type .env # Windows
```

### Frontend won't start

```bash
# Check Node version (requires 16+)
node --version

# Clean install
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Docker issues

```bash
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# View logs
docker-compose logs -f

# Check container status
docker-compose ps
```

**Common Docker Issues:**
- **SSL Certificate Errors**: Fixed in frontend Dockerfile with `npm config set strict-ssl false`
- **Port Conflicts**: Change ports in `.env` file and rebuild
- **Build Failures**: Run `docker system prune -f` then rebuild
- **Connection Issues**: Verify `REACT_APP_BACK_END_URL` is set correctly

See [docs/DOCKER_README.md](docs/DOCKER_README.md) for comprehensive troubleshooting.

### Tests failing

```bash
# Run tests with Docker (recommended)
.\docker-start.ps1 -Test

# View test logs
docker-compose -f docker-compose.test.yml logs backend-test
docker-compose -f docker-compose.test.yml logs frontend-test

# Run tests manually with verbose output
cd backend
pytest -vv

# Run specific test
pytest tests/test_tasks.py::TestTasksCRUD::test_create_task_success -v

# Rebuild test images
docker-compose -f docker-compose.test.yml build --no-cache
```

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 📧 Support

For questions or issues:
- Review documentation in `docs/` directory
- Check [Integration Guide](INTEGRATION_GUIDE.md)
- Consult team members based on area of expertise
- Review GitHub Actions logs for CI/CD issues

---

**Good luck, and have fun building! The instructional team is here to support you.** 🚀
