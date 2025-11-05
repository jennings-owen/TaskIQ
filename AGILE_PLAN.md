# Agile Sprint Plan: Agile TaskIQ

## Team Members & Roles

| Member | Role/Focus Area                |
|--------|-------------------------------|
| 1      | Database Design (schema.sql)  |
| 2      | Backend (API & Logic)         |
| 3      | Frontend (React UI)           |
| 4      | Integration & Testing         |

---

## User Stories & Tasks

### Member 1: Database Design (George)
- [ ] Design and implement `schema.sql` based on PRD database schema.
- [ ] Ensure tables: users, tasks, task_dependencies, task_priority_scores, task_tshirt_scores.
- [ ] Add constraints, indexes, and sample data if needed.

---

### Member 2: Backend Development (FastAPI) (Kristy)
- [ ] Set up FastAPI project structure.
- [ ] Implement CRUD endpoints for `/tasks` (GET, POST, PUT, DELETE).
- [ ] Implement `/ai/rank` endpoint for task priority scoring.
- [ ] Implement `/ai/size` endpoint for T-shirt size recommendation.
- [ ] Add CORS middleware for frontend integration.
- [ ] Connect backend to SQLite using SQLAlchemy.
- [ ] Write Pydantic models and validation logic.
- [ ] Document API endpoints (OpenAPI/Swagger).

---

### Member 3: Frontend Development (React) (Owen)
- [ ] Set up React project and install dependencies (axios, etc.).
- [ ] Create TaskList component to display tasks.
- [ ] Create TaskForm component for task creation/editing.
- [ ] Integrate API calls for CRUD operations.
- [ ] Display auto-generated priority scores in the UI.
- [ ] Create SizeRecommendationForm for T-shirt size feature.
- [ ] Add loading/error states and basic styling.

---

### Member 4: Integration, Testing, and Documentation (Lawrence)
- [ ] Write unit tests for backend endpoints (pytest).
- [ ] Test API integration with frontend (manual & automated).
- [ ] Identify and document security vulnerabilities.
- [ ] Write integration guide and update project documentation.
- [ ] Prepare sample data and demo scripts.
- [ ] Coordinate final bug fixes and polish.

---

## Sprint Milestones

1. **Day 1 Morning:** Database schema, backend scaffolding, frontend setup.
2. **Day 1 Afternoon:** Implement core endpoints, basic UI, initial integration.
3. **Day 2 Morning:** Testing, bug fixes, documentation, polish.
4. **Day 2 Afternoon:** Final integration, demo preparation, presentation.

---

## Notes

- Sync daily to review progress and blockers.
- Use GitHub issues or a Kanban board to track tasks.
- Each member should write/update relevant documentation for their area.

---
