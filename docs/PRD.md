# Product Requirements Document: Agile TaskIQ

| Status | **Draft** |
| :--- | :--- |
| **Author** | AI Business Analyst |
| **Version** | 1.0 |


# Table of Contents — PRD: Task Management System with Priority Intelligence

| Document | Link | Description |
|:---------|:-----|:------------|
| PRD.md   | This document | This is the overall product requirement document for the project. |
| SETUP.md | [Setup](./SETUP.md) | Information about environment setup, docker usage, and deployment. |
| AGILE_PLAN.md | [Plan](./AGILE_PLAN.md) | This document outlines all the tasks required to complete a MVP. |
| schema.sql | [Schema](../backend/schema.sql) | The initial SQLite schema file based on the constraints defined in this PRD. |
| seed_data.sql | [Data](../backend/seed_data.sql)| The SQL data used to populate the database. |
| database.db | [Database](../backend/database.db)| The SQL database. |
| ARCHITECTURE.md | [Architecture](./architecture.md) | Architecture design including UML diagrams. |
| ADR.md | [Architecture Design Record](./ADR.md) | Technical decisions with their justifications. |
| SECURITY_REVIEW.md | [Security Review](./SECURITY_REVIEW.md) | Security vulnerabilities report and recommendations. |
| UI/Wireframes | See /ui/ Folder | Draft UI generated using lab workflow, wireframes generated using Figma design. |
| CICD_PIPELINE.md | [CI/CD](./CICD_PIPELINE.md)| This describes the build pipeline used to create the project. |
| DOCKER_README.md | [DOCKER](./DOCKER_README.md)| This describes the build pipeline used to create the project. |
| ENV_FORMAT.md | [ENV](./ENV_FORMAT.md)| This describes the needed environment variables in the .env file to run the project. |

## 1. Executive Summary & Vision
Agile TaskIQ is a lightweight task management application designed to enhance productivity through AI-driven task prioritization. By integratinsg AI capabilities, the product aims to streamline task management for agile teams, software engineers, and consulting firms. The ultimate vision is to establish Agile TaskIQ as a leader in AI-enhanced task management solutions, offering unique features like T-shirt size recommendations to demonstrate AI capabilities and differentiate from competitors.

## 2. Problem Statement & Opportunity
The task management market is saturated with tools that lack advanced prioritization capabilities. Agile teams and consulting firms face challenges in efficiently prioritizing tasks, leading to decreased productivity. Agile TaskIQ addresses this gap by offering AI-driven task prioritization, providing a significant market opportunity to capture a growing segment of users seeking innovative solutions.

## 2A. Brainstorming Features

This section documents the AI-assisted brainstorming session conducted during the requirements phase. Features are categorized by user journey and implementation priority.

### Category 1: Core Task Management (MVP - Implemented)
*Goal: Provide essential task management functionality with AI enhancement*

* **Task CRUD Operations:** Create, read, update, and delete tasks with essential attributes (title, description, deadline, status, estimated duration).
* **AI Priority Scoring:** Automatically calculate and display a priority score (1-100) for each task based on deadline urgency and estimated effort.
* **Task Status Tracking:** Support for pending, in-progress, and completed states with visual indicators.
* **Task List View:** Sortable and filterable list view of all tasks with key information at a glance.
* **Task Details Panel:** Expandable panel showing full task information with inline editing capabilities.
* **User Authentication:** Secure login/registration system with JWT tokens to protect user data.

### Category 2: AI-Driven Intelligence (MVP - Implemented)
*Goal: Demonstrate AI capabilities for task complexity estimation and prioritization*

* **T-Shirt Size Estimation:** AI-powered Agile estimation that recommends task complexity (XS, S, M, L, XL) based on:
  - Task title and description analysis
  - Estimated duration
  - Presence of dependencies
  - Keyword detection (e.g., "refactor," "integrate," "design")
* **Batch Task Ranking:** Rank multiple tasks simultaneously to help with sprint planning.
* **Priority Score Visualization:** Color-coded priority indicators (red for high, yellow for medium, green for low).
* **AI Insights Panel:** Dedicated interface for viewing AI recommendations and explanations.

### Category 3: Collaboration & Dependencies (MVP - Implemented)
*Goal: Support team coordination and task relationships*

* **Task Dependencies:** Define which tasks depend on others to block or unblock work.
* **Dependency Visualization:** Graph view showing task relationships and blockers.
* **User Profile Management:** Allow users to update their name, email, and password.
* **Multi-User Support:** Each user has their own task workspace with secure data isolation.

### Category 4: Dashboard & Analytics (Future Enhancement)
*Goal: Provide insights into productivity patterns and team performance*

* **Productivity Dashboard:** Visual charts showing:
  - Tasks completed over time
  - Average time to completion vs. estimates
  - Most common priority score ranges
  - Task status distribution
* **AI Accuracy Tracking:** Show how accurate AI priority scores and size estimates were compared to actual completion times.
* **Burndown Charts:** Visualize progress toward sprint or project completion.
* **Team Performance Metrics:** For team leads to see overall team velocity and bottlenecks.

### Category 5: Advanced AI Features (Future Enhancement)
*Goal: Leverage machine learning for smarter predictions*

* **ML-Based Priority Prediction:** Train models on historical task completion data to improve priority score accuracy.
* **Time Estimate Refinement:** Learn from actual completion times to better estimate future tasks.
* **Smart Task Suggestions:** Recommend what to work on next based on priority, dependencies, and user work patterns.
* **Natural Language Task Creation:** "Create a task to refactor the authentication module by Friday" → auto-populates fields.
* **Sentiment Analysis:** Detect urgent or stressed language in task descriptions.
* **Thumbs Up/Down Feedback:** Allow users to rate AI suggestions to improve the model.

### Category 6: Integrations & Automation (Future Enhancement)
*Goal: Connect with existing tools and reduce manual work*

* **Calendar Integration:** Sync task deadlines with Google Calendar, Outlook, or iCal.
* **Slack/Teams Notifications:** Get notified when high-priority tasks are due soon.
* **GitHub/Jira Import:** Import issues from existing project management tools.
* **API Access:** Public API for third-party integrations.
* **Zapier/Make Integration:** Connect with thousands of other productivity apps.
* **Email-to-Task:** Forward an email to create a task automatically.

### Category 7: Customization & Personalization (Future Enhancement)
*Goal: Adapt to different team workflows and individual preferences*

* **Custom Task Fields:** Add fields like "Epic," "Story Points," "Assignee," or custom attributes.
* **Workflow Templates:** Pre-built task templates for common workflows (e.g., "Bug Fix Workflow," "Feature Development").
* **Personalized AI Settings:** Adjust how aggressively the AI prioritizes based on user preference.
* **Dark Mode:** Toggle between light and dark themes.
* **Keyboard Shortcuts:** Power-user shortcuts for rapid task creation and navigation.

### Category 8: Mobile & Accessibility (Future Enhancement)
*Goal: Enable task management on the go and for all users*

* **Mobile-Responsive Design:** Optimized UI for phones and tablets.
* **Native Mobile Apps:** iOS and Android apps for offline access.
* **Accessibility Compliance:** WCAG 2.1 AA compliance for screen readers and keyboard navigation.
* **Voice Commands:** "Show me my high-priority tasks" for hands-free use.

---

## 3. Target Users & Personas

Primary users include agile teams, software engineers, and consulting firms. These users are typically project managers, team leads, and individual contributors who struggle with task prioritization and require a user-friendly interface.

### Persona 1: Sarah Martinez, The Agile Team Lead

**Role:** Scrum Master at a mid-size software company

**Demographics:** 35 years old, 8 years of experience managing agile teams, manages a team of 7 developers

**Bio:**
Sarah runs two-week sprints and is constantly juggling competing priorities. Her team often struggles to agree on which stories to pull into a sprint because everyone has a different opinion on what's "urgent." She spends too much time in planning meetings debating task priority instead of actually executing. She's tech-savvy and loves tools that save her time.

**Goals:**
* Prioritize the sprint backlog with objective, data-driven criteria instead of gut feel.
* Reduce time spent in planning meetings by having AI pre-rank tasks.
* Quickly estimate task complexity to ensure the team doesn't over-commit.
* Help junior developers understand which tasks to tackle first.
* Track team velocity and identify bottlenecks.

**Frustrations (Pain Points):**
* **Subjective Prioritization:** Team debates endlessly about which task is more important.
* **Poor Estimation:** Developers routinely underestimate how long tasks will take.
* **Missed Deadlines:** High-priority tasks slip because they weren't flagged early enough.
* **Context Switching:** Constantly re-prioritizing when new urgent requests come in.
* **Manual Tracking:** Spreadsheets and sticky notes don't scale.

**How She Uses Agile TaskIQ:**
Sarah uses the tool daily for sprint planning and daily standups. She:
* Imports all backlog items at the start of sprint planning.
* Uses AI priority scoring to identify the top 10 tasks that should be in the sprint.
* Leverages t-shirt size estimates to ensure the team's capacity isn't exceeded.
* Shares the prioritized list with the team to align on commitments.
* Checks the dependency graph to avoid pulling in blocked tasks.

---

### Persona 2: Marcus Chen, The Individual Contributor

**Role:** Senior Software Engineer at a consulting firm

**Demographics:** 28 years old, 4 years of professional experience, works on multiple client projects simultaneously

**Bio:**
Marcus is a talented engineer who often works on 3-4 client projects at the same time. His biggest challenge is knowing what to work on next when everything feels urgent. He gets stressed when he has to choose between a high-value feature for Client A and a critical bug fix for Client B. He wants a system that can objectively tell him "this is the most important thing right now."

**Goals:**
* Get a clear, prioritized to-do list across multiple projects.
* Understand task complexity before committing to a deadline.
* Avoid burnout by focusing on high-impact work.
* Track his own productivity and learn from his estimation accuracy.
* Minimize time spent deciding what to work on.

**Frustrations (Pain Points):**
* **Overwhelming Workload:** Too many tasks from too many stakeholders.
* **Poor Estimation:** Commits to finishing a task in 2 hours, ends up taking 6.
* **Lack of Visibility:** Doesn't know which task will have the biggest impact.
* **Guilt:** Feels guilty when he picks the "easier" task instead of the "important" one.
* **No Learning Loop:** Doesn't improve his estimation skills because he never tracks actuals.

**How He Uses Agile TaskIQ:**
Marcus logs in every morning to see his personalized priority queue. He:
* Reviews the AI-calculated priority scores to know which task to start.
* Checks the t-shirt size estimate to gauge if he can finish it today.
* Updates task status (pending → in-progress → completed) as he works.
* Compares his actual time spent vs. the AI estimate to refine future predictions.
* Uses the dependency view to understand what's blocking his work.

---

### Persona 3: Lisa Tran, The Product Manager

**Role:** Product Manager at a fast-growing startup

**Demographics:** 42 years old, 15 years in product management, oversees 3 engineering teams

**Bio:**
Lisa is responsible for the product roadmap and ensuring the right features ship on time. She works with engineering, design, marketing, and sales—everyone wants their "urgent" task prioritized. She needs a way to objectively communicate to stakeholders why certain features are being delayed and others are being fast-tracked. She values transparency and data-backed decision-making.

**Goals:**
* Align cross-functional teams on what's most important.
* Communicate priority changes to stakeholders with data, not opinions.
* Ensure engineering resources are allocated to high-impact features.
* Track how long features actually take vs. initial estimates to improve future planning.
* Maintain a living roadmap that adapts to changing priorities.

**Frustrations (Pain Points):**
* **Stakeholder Pressure:** Everyone thinks their request is the most important.
* **Lack of Transparency:** Teams don't understand why decisions were made.
* **Estimation Inaccuracy:** Roadmap commitments slip because estimates were wrong.
* **Competing Priorities:** New "urgent" requests derail planned work constantly.
* **Manual Reporting:** Spends hours creating status reports instead of strategizing.

**How She Uses Agile TaskIQ:**
Lisa uses the tool for roadmap planning and stakeholder communication. She:
* Adds all feature requests and assigns deadlines.
* Uses AI priority scores to build a data-backed roadmap.
* Shares the prioritized backlog in planning meetings to justify decisions.
* Tracks actual completion times to improve future estimates.
* Generates reports showing which features shipped and which were deprioritized.

## 4. Success Metrics & Goals
Key performance indicators (KPIs) include user adoption rates, task prioritization accuracy, and user satisfaction scores. Success will be measured by the ability to generate accurate priority scores, seamless integration with existing workflows, and positive user feedback on the AI capabilities.

## 5. Functional Requirements & User Stories

This section documents detailed user stories with acceptance criteria in Given/When/Then format, generated during the AI-assisted requirements phase.

### User Story 1: Task Creation with AI Priority Scoring

**ID:** US-001  
**Persona:** Marcus Chen, The Individual Contributor  
**User Story:** As an Individual Contributor, I want to create a new task with a title, description, deadline, and estimated duration, so that I can track my work and receive an AI-calculated priority score automatically.

**Acceptance Criteria:**
* **Given** I am logged into Agile TaskIQ,  
  **When** I click the "Create Task" button,  
  **Then** a task creation dialog should appear with fields for title, description, deadline, estimated duration, and status.
  
* **Given** I have filled in all required fields (title, deadline, estimated duration),  
  **When** I click "Save Task",  
  **Then** the system should automatically calculate and assign a priority score (1-100) based on the deadline urgency and estimated effort.
  
* **Given** I have successfully created a task,  
  **When** I return to the task list view,  
  **Then** the new task should appear in the list with its calculated priority score displayed prominently.
  
* **Given** I create a task with a very close deadline (e.g., tomorrow),  
  **When** the priority score is calculated,  
  **Then** the score should be high (80-100) and displayed in red to indicate urgency.

---

### User Story 2: View All Tasks with Priority Sorting

**ID:** US-002  
**Persona:** Sarah Martinez, The Agile Team Lead  
**User Story:** As an Agile Team Lead, I want to view all tasks in a sortable list with their priority scores visible, so that I can quickly identify which tasks my team should focus on first.

**Acceptance Criteria:**
* **Given** I am logged into the system,  
  **When** I navigate to the "Tasks" view,  
  **Then** I should see a list of all tasks with columns for title, status, deadline, estimated duration, and priority score.
  
* **Given** I am viewing the task list,  
  **When** I click the "Priority Score" column header,  
  **Then** the tasks should sort in descending order (highest priority first).
  
* **Given** I have tasks with varying priority scores,  
  **When** I view the list,  
  **Then** tasks with scores 70-100 should have a red indicator, 40-69 should have a yellow indicator, and 1-39 should have a green indicator.
  
* **Given** I have more than 10 tasks,  
  **When** I scroll through the list,  
  **Then** the interface should support smooth scrolling and display all tasks without pagination errors.

---

### User Story 3: AI T-Shirt Size Estimation

**ID:** US-003  
**Persona:** Sarah Martinez, The Agile Team Lead  
**User Story:** As an Agile Team Lead, I want to receive an AI-generated t-shirt size recommendation (XS, S, M, L, XL) for any task, so that I can quickly estimate complexity during sprint planning.

**Acceptance Criteria:**
* **Given** I have selected a task from my task list,  
  **When** I navigate to the "AI Tools" panel and click "Get Size Estimate",  
  **Then** the system should analyze the task's title, description, estimated duration, and dependencies to recommend a t-shirt size.
  
* **Given** a task has a short estimated duration (1-2 hours) and simple description,  
  **When** I request a size estimate,  
  **Then** the system should recommend "XS" or "S".
  
* **Given** a task has a long estimated duration (8+ hours), complex keywords (e.g., "refactor," "integrate"), and dependencies,  
  **When** I request a size estimate,  
  **Then** the system should recommend "L" or "XL".
  
* **Given** I receive a t-shirt size recommendation,  
  **When** I view the result,  
  **Then** the system should display a brief rationale explaining why that size was recommended.

---

### User Story 4: Update Task Status

**ID:** US-004  
**Persona:** Marcus Chen, The Individual Contributor  
**User Story:** As an Individual Contributor, I want to update a task's status from "pending" to "in-progress" to "completed", so that I can track my progress and keep my team informed.

**Acceptance Criteria:**
* **Given** I have selected a task from my task list,  
  **When** I click on the task to open the details panel,  
  **Then** I should see a status dropdown with options: "pending," "in-progress," and "completed".
  
* **Given** I change a task's status from "pending" to "in-progress",  
  **When** I save the change,  
  **Then** the task list should immediately reflect the updated status.
  
* **Given** I mark a task as "completed",  
  **When** I view the task list,  
  **Then** the completed task should have a visual indicator (e.g., strikethrough or checkmark).
  
* **Given** I update a task's status,  
  **When** the change is saved,  
  **Then** the task's "updated_at" timestamp should be refreshed to the current time.

---

### User Story 5: Delete a Task

**ID:** US-005  
**Persona:** Marcus Chen, The Individual Contributor  
**User Story:** As an Individual Contributor, I want to delete a task that is no longer relevant, so that my task list remains clean and focused.

**Acceptance Criteria:**
* **Given** I have selected a task from my task list,  
  **When** I click the "Delete" button in the task details panel,  
  **Then** the system should prompt me with a confirmation dialog saying "Are you sure you want to delete this task?"
  
* **Given** I confirm the deletion,  
  **When** I click "Yes, Delete",  
  **Then** the task should be permanently removed from the database and disappear from my task list.
  
* **Given** I accidentally click "Delete",  
  **When** I see the confirmation dialog,  
  **Then** I should be able to click "Cancel" to abort the deletion.
  
* **Given** I delete a task that has dependencies,  
  **When** the task is removed,  
  **Then** the system should also remove any associated dependency records to maintain database integrity.

---

### User Story 6: User Registration and Authentication

**ID:** US-006  
**Persona:** Marcus Chen, The Individual Contributor  
**User Story:** As a new user, I want to register for an account with my name, email, and password, so that I can securely access my personal task workspace.

**Acceptance Criteria:**
* **Given** I am on the login page,  
  **When** I click "Register",  
  **Then** I should be taken to a registration form with fields for name, email, and password.
  
* **Given** I fill in all registration fields with valid data,  
  **When** I click "Create Account",  
  **Then** the system should hash my password using bcrypt and store my account in the database.
  
* **Given** I have successfully registered,  
  **When** the account is created,  
  **Then** I should be automatically logged in and receive a JWT token for authentication.
  
* **Given** I try to register with an email that already exists,  
  **When** I submit the form,  
  **Then** I should see an error message: "Email already registered."

---

### User Story 7: User Login

**ID:** US-007  
**Persona:** Sarah Martinez, The Agile Team Lead  
**User Story:** As a returning user, I want to log in with my email and password, so that I can securely access my task workspace and see only my tasks.

**Acceptance Criteria:**
* **Given** I am on the login page,  
  **When** I enter my registered email and correct password,  
  **Then** I should be authenticated and redirected to my task list.
  
* **Given** I successfully log in,  
  **When** the authentication completes,  
  **Then** I should receive a JWT token that is stored in my browser and used for all subsequent API requests.
  
* **Given** I enter an incorrect password,  
  **When** I click "Login",  
  **Then** I should see an error message: "Incorrect email or password."
  
* **Given** I am logged in,  
  **When** I navigate to any protected route (e.g., "/tasks"),  
  **Then** the system should verify my JWT token and grant access only if the token is valid.

---

### User Story 8: Define Task Dependencies

**ID:** US-008  
**Persona:** Sarah Martinez, The Agile Team Lead  
**User Story:** As an Agile Team Lead, I want to define which tasks depend on other tasks, so that my team understands blockers and can plan their work accordingly.

**Acceptance Criteria:**
* **Given** I am viewing a task's details,  
  **When** I click "Add Dependency",  
  **Then** I should see a dropdown list of all other tasks that this task could depend on.
  
* **Given** I select a task as a dependency,  
  **When** I save the change,  
  **Then** a new dependency record should be created in the database linking the two tasks.
  
* **Given** a task has dependencies,  
  **When** I view the task details,  
  **Then** I should see a list of all tasks it depends on with their titles and statuses.
  
* **Given** I delete a task that is a dependency for another task,  
  **When** the deletion occurs,  
  **Then** the dependency relationship should be removed automatically (cascade delete).

---

### User Story 10: Update Profile Information

**ID:** US-010  
**Persona:** Marcus Chen, The Individual Contributor  
**User Story:** As a user, I want to update my profile name and email, so that my account information stays current.

**Acceptance Criteria:**
* **Given** I am logged in,  
  **When** I navigate to the "Profile" or "Settings" page,  
  **Then** I should see a form with my current name and email pre-filled.
  
* **Given** I change my name or email,  
  **When** I click "Save Changes",  
  **Then** the system should update my user record in the database.
  
* **Given** I try to change my email to one that is already registered by another user,  
  **When** I submit the form,  
  **Then** I should see an error: "Email already in use."
  
* **Given** I successfully update my profile,  
  **When** the save completes,  
  **Then** I should see a success message: "Profile updated successfully."

## 6. Non-Functional Requirements (NFRs)
- The system should be performant, with task prioritization and size recommendation responses within 200ms.
- Ensure data privacy and security compliance, particularly with user data handling.
- The application should be scalable to accommodate future feature expansions.

## 7. Release Plan & Milestones
- Hour 1: Setup FastAPI, SQLite, and models.
- Hour 2: Implement CRUD endpoints for /tasks.
- Hour 3: Setup React with TaskList and TaskForm.
- Hour 4: Integrate backend APIs in frontend.
- Hour 5: Add enhanced UI components and features.
- Hour 6: Testing, bug fixes, documentation.

## 8. Out of Scope & Future Considerations
- Advanced AI features such as machine learning-based prioritization are out of scope for the MVP.
- Future releases may include integrations with third-party tools and enhanced analytics.

## 9. Appendix & Open Questions & Future Steps
- Dependencies include FastAPI, React, and SQLite.
- Open questions: What additional AI features could enhance user experience in future iterations?
- Add ability to rank AI suggestions with thumbs up and down.
- Add ability to input the final time required to complete task when completed to help with training the AI in the future.
- Improve ranking of tasks through AI. Use more advanced ranking criteria, crewAI, or langchain to analyze the tasks.
- Can allow users to share tasks with other users.

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
