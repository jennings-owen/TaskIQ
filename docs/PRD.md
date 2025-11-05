# Product Requirements Document: Agile TaskIQ

| Status | **Draft** |
| :--- | :--- |
| **Author** | AI Business Analyst |
| **Version** | 1.0 |


# Table of Contents — PRD: Task Management System with Priority Intelligence

| Document | Link | Description |
|:---------|:-----|:------------|
| PRD.md   | This document | This is the overall product requirement document for the project. |
| PRD_AI_DRAFT.md | [Draft](./PRD_AI_DRAFT.md) | This is the original AI generated PRD document. It serves as the baseline for this final PRD document. |
| SETUP.md | [Setup](./SETUP.md) | Information about environment setup, docker usage, and deployment. |
| AGILE_PLAN.md | [Plan](./AGILE_PLAN.md) | This document outlines all the tasks required to complete a MVP. |
| schema.sql | [Schema](../backend/schema.sql) | The initial SQLite schema file based on the constraints defined in this PRD. |
| seed_data.sql | [Data](../backend/seed_data.sql)| The SQL data used to populate the database. |
| team_synapse.db | [Database](../backend/team_synapse.db)| The SQL database. |
| ARCHITECTURE.md | [Architecture](./architecture.md) | Architecture design including UML diagrams. |
| ADR.md | [Architecture Design Record](./ADR.md) | Technical decisions with their justifications. |
| UI/Wireframes | See /ui/ Folder | Draft UI generated using lab workflow, wireframes generated using Figma design. |

## 1. Executive Summary & Vision
Agile TaskIQ is a lightweight task management application designed to enhance productivity through AI-driven task prioritization. By integrating AI capabilities, the product aims to streamline task management for agile teams, software engineers, and consulting firms. The ultimate vision is to establish Agile TaskIQ as a leader in AI-enhanced task management solutions, offering unique features like T-shirt size recommendations to demonstrate AI capabilities and differentiate from competitors.

## 2. Problem Statement & Opportunity
The task management market is saturated with tools that lack advanced prioritization capabilities. Agile teams and consulting firms face challenges in efficiently prioritizing tasks, leading to decreased productivity. Agile TaskIQ addresses this gap by offering AI-driven task prioritization, providing a significant market opportunity to capture a growing segment of users seeking innovative solutions.

## 3. Target Users & Personas
Primary users include agile teams, software engineers, and consulting firms. These users are typically project managers, team leads, and individual contributors who struggle with task prioritization and require a user-friendly interface. Their motivations include enhancing team productivity, integrating AI tools, and simplifying task management processes.

## 4. Success Metrics & Goals
Key performance indicators (KPIs) include user adoption rates, task prioritization accuracy, and user satisfaction scores. Success will be measured by the ability to generate accurate priority scores, seamless integration with existing workflows, and positive user feedback on the AI capabilities.

## 5. Functional Requirements & User Stories
- As a user, I want to create, view, update, and delete tasks so that I can manage my workload effectively.
  - Acceptance Criteria: Users can perform CRUD operations via a REST API and view tasks in a React list view.
- As a user, I want to see an auto-generated priority score for each task to prioritize my work efficiently.
  - Acceptance Criteria: The system automatically calculates and displays a priority score (1-100) for each task.
- As a user, I want to receive a T-shirt size recommendation based on my attributes for quick decision-making.
  - Acceptance Criteria: The /ai/size endpoint returns a recommended T-shirt size based on user input.

## 6. Non-Functional Requirements (NFRs)
- The system should be performant, with task prioritization and size recommendation responses within 200ms.
- Ensure data privacy and security compliance, particularly with user data handling.
- The application should be scalable to accommodate future feature expansions.

## 7. Release Plan & Milestones
- Hour 1: Setup FastAPI, SQLite, and models.
- Hour 2: Implement CRUD endpoints for /tasks.
- Hour 3: Implement /ai/rank scoring logic.
- Hour 4: Implement /ai/size endpoint.
- Hour 5: Setup React with TaskList and TaskForm.
- Hour 6: Integrate backend APIs in frontend.
- Hour 7: Add PriorityDashboard and SizeRecommendationForm.
- Hour 8: Testing, bug fixes, documentation.

## 8. Out of Scope & Future Considerations
- Advanced AI features such as machine learning-based prioritization are out of scope for the MVP.
- Future releases may include integrations with third-party tools and enhanced analytics.

## 9. Appendix & Open Questions
- Dependencies include FastAPI, React, and SQLite.
- Open questions: What additional AI features could enhance user experience in future iterations?

## 10. API Design
1. /tasks (CRUD)

Endpoints:

GET /tasks – Get all tasks.

POST /tasks – Create a new task.

PUT /tasks/{id} – Update a task.

DELETE /tasks/{id} – Delete a task.

Task Model Example:
```json
{
  "id": 1,
  "title": "Submit project report",
  "description": "Send final report to manager",
  "deadline": "2025-11-06",
  "status": "pending",
  "estimated_duration": 4,
  "priority_score": 85
}
```
2. /ai/rank (Task Priority Scoring)

POST Request:
```json
{
  "tasks": [
    {
      "title": "Submit project report",
      "deadline": "2025-11-06",
      "estimated_duration": 4
    },
    {
      "title": "Clean workspace",
      "deadline": "2025-11-15",
      "estimated_duration": 1
    }
  ]
}
```

Response:
```json
[
  {"task_id": 1, "priority_score": 92},
  {"task_id": 2, "priority_score": 45}
]
```

Logic (simplified for 1-day scope):

Score = 100 - days_until_deadline * 5 - estimated_duration * 3

Clamped between 1 and 100.

3. /ai/size (T-shirt Size Recommendation)

POST Request:
```json
{
  "height_cm": 175,
  "weight_kg": 70,
  "gender": "male",
  "fit_preference": "regular"
}
```

Response:
```json
{"recommended_size": "M"}
```

## 11. Database Schema

1. users

| Field         | Type     | Constraints               | Description                 |
| ------------- | -------- | ------------------------- | --------------------------- |
| id            | INTEGER  | PRIMARY KEY               | Unique user ID              |
| name          | TEXT     | NOT NULL                  | User’s display name         |
| email         | TEXT     | UNIQUE NOT NULL           | User email address          |
| password_hash | TEXT     | NULLABLE                  | Optional password for login |
| created_at    | DATETIME | DEFAULT CURRENT_TIMESTAMP | Account creation timestamp  |

2. tasks

| Field              | Type     | Constraints               | Description                       |
| ------------------ | -------- | ------------------------- | --------------------------------- |
| id                 | INTEGER  | PRIMARY KEY               | Task ID                           |
| user_id            | INTEGER  | FOREIGN KEY → users(id)   | Owner of the task                 |
| title              | TEXT     | NOT NULL                  | Task name                         |
| description        | TEXT     | NULLABLE                  | Task details                      |
| deadline           | DATETIME | NULLABLE                  | Due date                          |
| estimated_duration | INTEGER  | NULLABLE                  | Estimated hours to complete       |
| status             | TEXT     | DEFAULT 'pending'         | pending / in_progress / completed / |
| created_at         | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation time              |
| updated_at         | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record update time                |

3. task_dependencies

| Field              | Type    | Constraints             | Description        |
| ------------------ | ------- | ----------------------- | ------------------ |
| id                 | INTEGER | PRIMARY KEY             | Record ID          |
| task_id            | INTEGER | FOREIGN KEY → tasks(id) | The main task      |
| depends_on_task_id | INTEGER | FOREIGN KEY → tasks(id) | Task it depends on |


4. task_priority_scores

| Field             | Type     | Constraints               | Description                          |
| ----------------- | -------- | ------------------------- | ------------------------------------ |
| id                | INTEGER  | PRIMARY KEY               | Record ID                            |
| task_id           | INTEGER  | FOREIGN KEY → tasks(id)   | Task being scored                    |
| score             | INTEGER  | NOT NULL                  | AI-calculated priority score (1–100) |

5. task_tshirt_scores

| Field             | Type     | Constraints               | Description                  |
| ----------------- | -------- | ------------------------- | ---------------------------- |
| id                | INTEGER  | PRIMARY KEY               | Record ID                    |
| task_id           | INTEGER  | FOREIGN KEY → tasks(id)   | Task being evaluated         |
| tshirt_size       | TEXT     | NOT NULL                  | XS / S / M / L / XL          |
| rationale         | TEXT     | NULLABLE                  | AI explanation or reasoning  |


## 12. Documentation Requirements

- [**Architecture Document**](docs/ARCHITECTURE.md): System architecture overview with PlantUML diagrams (component and sequence) showing React frontend, FastAPI backend, SQLite database, and API interactions. Reference Section 10 (API Design) and Section 11 (Database Schema).

- [**Architecture Decision Records**](docs/ADR.md): Consolidated technical decisions including database selection (SQLite with 5 tables per Section 11), rule-based priority algorithm, modular API architecture, and frontend framework (React + Tailwind).

- [**Security Audit Report**](docs/SECURITY.md): Vulnerability assessment covering SQL injection risks, input validation for all endpoints (Section 10), authentication gaps (users table per Section 11), CORS configuration, and mitigation strategies.

- [**Agile Plan**](docs/AGILE_PLAN.md): Granular task list expanding Section 7 (Release Plan) into actionable items with dependencies and acceptance criteria for each milestone.

- [**AI Artifact Log**](docs/AI_GENERATION_LOG.md): Comprehensive record of AI prompts and outputs for PRD generation, schema.sql creation, API code generation, test suite creation, and security audit. Demonstrates AI integration across SDLC.

## 13. Testing Suite

- [**Backend Unit Tests**](backend/tests/test_main.py): Pytest suite covering all CRUD endpoints (Section 10), AI ranking logic with edge cases (line 119 algorithm validation), size recommendation endpoint, and database operations across all 5 tables (Section 11). 

- [**Frontend Component Tests**](frontend/src/__tests__/): React Testing Library tests for TaskList, TaskForm, and Dashboard components (per Section 12 directory structure). Verify API integration, priority score display, and error handling.

- [**Integration Tests**](backend/tests/test_integration.py): Full task lifecycle with user authentication, task dependencies (task_dependencies table), priority score generation (task_priority_scores table), and t-shirt size scoring (task_tshirt_scores table). 

- [**Database Tests**](backend/tests/test_database.py): Validate foreign key constraints, cascade deletes, timestamp auto-generation, and referential integrity across users, tasks, task_dependencies, task_priority_scores, and task_tshirt_scores tables.
