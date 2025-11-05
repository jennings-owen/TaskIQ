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
- **Status:** Pending
- **Context:** Database schema is being designed (see schema.sql).
- **Decision:** [To be updated after schema.sql is finalized]
- **Consequences:** [To be updated]

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

---

## Notes
- This ADR file will be updated with schema-specific decisions once schema.sql is available.
- Security audit/report will be maintained as a living document (see PRD Section 13 and SECURITY.md).
