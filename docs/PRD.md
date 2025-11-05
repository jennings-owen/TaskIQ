# Product Requirements Document: Agile TaskIQ

| Status | **Draft** |
| :--- | :--- |
| **Author** | AI Business Analyst |
| **Version** | 1.0 |

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


Database schema: 
Table: tasks
Field	Type	Description
id	Integer (PK)	Auto-increment
title	Text	Task title
description	Text	Task details
deadline	DateTime	Task due date
estimated_duration	Integer	Duration (hours)
status	Text	pending/in_progress/completed
priority_score	Integer	Calculated AI score

... to continue
```
