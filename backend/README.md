# Backend API — Quick Handoff

This document summarizes the backend HTTP API for quick handoff to frontend or training/data engineers.

## Run the server

Start the development server (from repository root):

```pwsh
uvicorn backend.app.main:app --reload
```

The SQLite DB used by the service (seeded for development) is at `backend/team_synapse.db`.

## Endpoints (summary)

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

- `POST /ai/size` — Agile t-shirt size estimation for tasks (ephemeral)
  - Estimates task complexity/effort using t-shirt sizes (XS, S, M, L, XL)
  - Request: `{"title": "string", "description": "optional", "estimated_duration": int, "has_dependencies": bool}`
  - Returns: `{"recommended_size": "M", "rationale": "explanation"}`
  - Ephemeral estimation only; use `/tasks/{task_id}/ai/size` to persist

- `POST /tasks/{task_id}/ai/size` — compute and persist t-shirt size for existing task
  - Analyzes task attributes (title, description, duration, dependencies) to estimate complexity
  - Query param `?persist=true` (default) will upsert into `task_tshirt_scores`
  - Returns size (XS/S/M/L/XL) based on Agile estimation factors

## Example requests

- Minimal create (curl):

```pwsh
curl -X POST "http://127.0.0.1:8000/tasks" -H "Content-Type: application/json" -d '{"title":"Create landing page"}'
```

- Full create (curl):

```pwsh
curl -X POST "http://127.0.0.1:8000/tasks" -H "Content-Type: application/json" -d '{"title":"Implement login","description":"OAuth 2.0","deadline":"2025-11-20T17:00:00Z","estimated_duration":8}'
```

- Estimate t-shirt size for a task (ephemeral):

```pwsh
curl -X POST "http://127.0.0.1:8000/api/ai/size" -H "Content-Type: application/json" -d '{"title":"Implement OAuth integration","description":"Add OAuth 2.0 providers","estimated_duration":12,"has_dependencies":true}'
```

- Compute and persist t-shirt size for existing task 1:

```pwsh
curl -X POST "http://127.0.0.1:8000/api/tasks/1/ai/size?persist=true"
```

## Response examples

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

## Notes and guidance

- Validation and error codes
  - 400: client-supplied `user_id` does not exist or other client validation errors
  - 404: task not found for GET/PUT/DELETE
  - 422: Pydantic validation errors (invalid datetimes, wrong types)

- Behavior choices
  - For now the API accepts optional/blank values and coerces empty strings for `deadline` and `estimated_duration` to `null` to be forgiving to frontend forms.
  - The server currently creates/uses a default `system@local` user when `user_id` is omitted. If you plan to require authentication, make `user_id` required and return 400 when missing.

- DB and migrations
  - The project includes SQLAlchemy models. If you change models in production, add Alembic migrations. SQLite has limited ALTER support — a typical migration may require table copy/recreate.

## Running tests

Run the backend tests (fast):

```pwsh
pytest backend/tests -q
```

## Contact points

If frontend engineers need more fields, add them to Pydantic models in `backend/app/schemas.py` and the database models in `backend/app/models.py`. Coordinate schema changes with the team and add an Alembic migration.
