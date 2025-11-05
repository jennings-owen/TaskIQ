#  Capstone Project: AI-Driven Software Engineering

Welcome to the final project for the AI-Driven Software Engineering Program! This two-day capstone is your opportunity to synthesize all the skills you've acquired over the past eight days. You will apply AI-assisted techniques across the entire software development lifecycle to build a complete, functional application from the ground up.

## Quick Start

### Three Operating Modes

**1. Production Mode (Default)**
```powershell
.\docker-start.ps1          # Windows
./docker-start.sh           # Linux/Mac
```
Optimized production build, runs in detached mode.

**2. Development Mode**
```powershell
.\docker-start.ps1 -Dev     # Windows
./docker-start.sh -Dev      # Linux/Mac
```
Hot-reload enabled, code changes reflected immediately.

**3. Test Mode**
```powershell
.\docker-start.ps1 -Test    # Windows
./docker-start.sh -Test     # Linux/Mac
```
Runs full test suite (192+ tests) with coverage reporting.

### Access Points
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Documentation
- **Docker Guide**: [DOCKER_START_GUIDE.md](DOCKER_START_GUIDE.md) - Complete Docker usage guide
- **Manual Setup**: [docs/SETUP.md](docs/SETUP.md) - Non-Docker installation
- **Test Suite**: [docs/TEST_SUITE_OVERVIEW.md](docs/TEST_SUITE_OVERVIEW.md) - Complete test documentation
- **CI/CD Pipeline**: [docs/CICD_PIPELINE.md](docs/CICD_PIPELINE.md) - Pipeline and testing details
- **Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design
- **Product Requirements**: [docs/PRD.md](docs/PRD.md) - Product specification
- **Agile Plan**: [docs/AGILE_PLAN.md](docs/AGILE_PLAN.md) - Sprint plan and team responsibilities

---

## 🎯 Project Goal

The primary goal of this capstone is to **build and present a working prototype of a software application, demonstrating the integration of Generative AI at every phase of the SDLC**. You will act as a full-stack developer, using AI as your co-pilot for planning, architecture, coding, testing, and documentation.

---

##  deliverables Checklist

Your final submission must include the following components. You will use AI assistance to generate and refine each of these artifacts.

* **Documentation:**
    * `Product Requirements Document (PRD)` generated from a high-level idea.
    * `Architecture Document` including auto-generated UML diagrams (e.g., Component or Sequence diagrams).
    * `Architecture Decision Records (ADR)` including auto-generated technical decisions with their justifications.
* **Backend Application:**
    * A complete REST API project using **Python and FastAPI**.
    * An AI-generated database schema (e.g., `schema.sql`).
    * A suite of **unit tests** generated with AI assistance.
    * A report or list of identified **security vulnerabilities**.
* **Frontend Application:**
    * A **React** frontend that interacts with your backend API.
    * At least one key component generated from a **design screenshot or mockup**.
* **Final Presentation:**
    * A **10-15 minute presentation** summarizing your project.
    * A **live demo** of your fully working front-end and back-end application.
* **AI Code:**
    * A **ipynb or py file(s)** containing the code you used to generate your artifacts.

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

### Security Features

- Input validation using Pydantic schemas
- CORS configuration for frontend integration
- SQL injection protection via SQLAlchemy ORM
- Comprehensive security review documentation

### Security Scanning

The project includes automated security scanning via GitHub Actions:

- **Bandit**: Python security linter
- **Safety**: Dependency vulnerability checker
- **CodeQL**: Advanced code analysis
- **Trivy**: Container security scanning

### Known Limitations (MVP)

- No authentication/authorization (suitable for demo only)
- Deploy only in trusted environments
- See [Security Review](docs/SECURITY_REVIEW.md) for complete assessment

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
Agile-TaskIQ/
├── .github/
│   └── workflows/           # CI/CD workflows
│       ├── ci.yml          # Main CI/CD pipeline
│       ├── security.yml    # Security scanning
│       └── README.md       # Workflow documentation
├── backend/
│   ├── main.py             # FastAPI application
│   ├── tests/              # Test suite
│   │   ├── conftest.py    # Test fixtures
│   │   ├── test_tasks.py  # Task endpoint tests
│   │   └── test_ai.py     # AI endpoint tests
│   ├── Dockerfile          # Backend container
│   └── Dockerfile.dev      # Development container
├── frontend/
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   └── ...
│   ├── Dockerfile         # Frontend container
│   └── package.json       # Node dependencies
├── docs/
│   ├── PRD.md             # Product Requirements Document
│   ├── AGILE_PLAN.md      # Sprint plan
│   ├── API_REFERENCE.md   # API documentation
│   ├── TESTING_GUIDE.md   # Testing instructions
│   ├── SECURITY_REVIEW.md # Security assessment
│   └── INTEGRATION_TEST_CHECKLIST.md
├── docker-compose.yml     # Container orchestration
├── requirements.txt       # Python dependencies
└── README.md             # This file
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

<<<<<<< HEAD
Good luck, and have fun building! The instructional team is here to support you.

---

## Backend API — Quick Handoff

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
=======
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
docker-compose up
```

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

Good luck, and have fun building! The instructional team is here to support you.
>>>>>>> 92b2413599b8925cbf328e18f601c8a22c5297be
