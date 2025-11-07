# Architecture Decision Records (ADR): Agile TaskIQ
## ADR-000: Frontend Framework & Styling
- **Status:** Accepted
- **Context:** Need for a modern, component-based UI framework with strong ecosystem and support for rapid prototyping.
- **Decision:** Use React for frontend, with Tailwind CSS for styling (as needed).
- **Consequences:** Fast UI development, reusable components, easy integration with backend APIs.

## ADR-006: Testing Strategy
- **Status:** Accepted
- **Context:** Need for robust, automated testing for both backend and frontend.
- **Decision:** Use pytest for backend unit/integration tests; use Jest and React Testing Library for frontend tests.
- **Consequences:** Improved code quality, easier refactoring, confidence in releases.

## ADR-007: Containerization & Deployment
- **Status:** Accepted
- **Context:** Need for consistent development and deployment environments.
- **Decision:** Use Docker for local development and deployment (see README and Docker guide).
- **Consequences:** Simplifies onboarding, ensures consistency, enables future CI/CD integration.


## ADR-001: Technology Stack
- **Status:** Accepted
- **Context:** Need for rapid MVP development with modern, well-supported tools.
- **Decision:** Use FastAPI (Python) for backend, React for frontend, SQLite for database (MVP), SQLAlchemy as ORM.
- **Consequences:** Fast development, easy onboarding, future migration possible.

## ADR-002: API Design
- **Status:** Accepted
- **Context:** Need for clear, maintainable API for frontend-backend communication.
- **Decision:** Use RESTful API endpoints for all CRUD and AI operations.
- **Consequences:** Simplicity, wide compatibility, easy documentation.

## ADR-003: Database Schema
## ADR-003: Database Schema
- **Status:** Accepted
- **Context:** A finalized SQLite schema (`backend/schema.sql`) and seeded database (`backend/database.db`) are available for the MVP.
- **Decision:** Use the provided SQLite schema and `database.db` for the MVP. The schema includes tables: `users`, `tasks`, `task_dependencies`, `task_priority_scores`, and `task_tshirt_scores` with appropriate constraints and foreign keys as defined in `backend/schema.sql`.
- **Consequences:** The backend will use SQLAlchemy models that mirror the schema; migrations can be added later with Alembic if the schema evolves.

## ADR-004: Security & Validation
- **Status:** Accepted
- **Context:** Need to protect user data and ensure data integrity.
- **Decision:** Use Pydantic for input validation, enable CORS, follow security best practices.
- **Consequences:** Improved security, easier debugging, safer API.

## ADR-005: AI Logic Implementation
- **Status:** Accepted
- **Context:** Need for simple, explainable AI features in MVP.
- **Decision:** Implement rule-based logic for task ranking and T-shirt size recommendation.
- **Consequences:** Fast implementation, easy to explain, can be upgraded to ML in future.

## ADR-008: Authentication & Security
- **Status:** Accepted
- **Context:** Need for secure user authentication and data protection.
- **Decision:** 
  - Use JWT (JSON Web Tokens) for stateless authentication
  - Implement bcrypt password hashing with SHA256 fallback
  - Require SECRET_KEY environment variable with default for development
  - Enable CORS for frontend-backend communication
- **Consequences:** Secure authentication, password protection, flexible for both dev and production environments.

## ADR-009: SECRET_KEY Configuration
- **Status:** Accepted
- **Context:** Need to balance security with developer experience for course project.
- **Decision:** Make SECRET_KEY optional with a safe default value for development, but issue warning when default is used.
- **Consequences:** 
  - Developers can run the app without configuration
  - Production deployments are encouraged to set custom SECRET_KEY
  - Warning reminds developers about security best practices

---

## Cross-References
- [Product Requirements Document](./PRD.md)
- [Architecture Document](./ARCHITECTURE.md)
- [Security Review Report](./SECURITY_REVIEW.md)
- [Database Schema](../backend/schema.sql)
