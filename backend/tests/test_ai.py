import json
import sqlite3
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_ai_rank_non_persist():
    payload = {
        "tasks": [
            {"title": "Test task", "deadline": "2025-11-10T00:00:00Z", "estimated_duration": 2}
        ]
    }
    r = client.post("/ai/rank", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert "priority_score" in data[0] or "priority_score" in data[0]


def test_ai_rank_persist():
    # use an existing task id from seed data (1)
    payload = {
        "tasks": [
            {"task_id": 1, "title": "Implement user authentication endpoint", "deadline": "2024-11-25T17:00:00Z", "estimated_duration": 8}
        ]
    }
    r = client.post("/ai/rank?persist=true", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data[0]["task_id"] == 1

    # check DB that the score was persisted
    conn = sqlite3.connect("backend/team_synapse.db")
    cur = conn.cursor()
    cur.execute("SELECT score FROM task_priority_scores WHERE task_id = ?", (1,))
    row = cur.fetchone()
    conn.close()
    assert row is not None

