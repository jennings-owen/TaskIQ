from backend.app.main import app
from fastapi.testclient import TestClient
import sqlite3

client = TestClient(app)


def test_create_update_delete_task():
    # Create
    payload = {"title": "crud-smoke", "description": "smoke test", "estimated_duration": 3}
    r = client.post("/tasks", json=payload)
    assert r.status_code == 200
    created = r.json()
    assert created["title"] == payload["title"]
    task_id = created["id"]

    # Update
    update_payload = {"title": "crud-smoke-updated", "estimated_duration": 5}
    r2 = client.put(f"/tasks/{task_id}", json=update_payload)
    assert r2.status_code == 200
    updated = r2.json()
    assert updated["title"] == update_payload["title"]
    assert updated["estimated_duration"] == update_payload["estimated_duration"]

    # Delete
    r3 = client.delete(f"/tasks/{task_id}")
    assert r3.status_code == 200
    assert r3.json().get("ok") is True

    # Confirm delete returns 404 on subsequent delete or get via update
    r4 = client.put(f"/tasks/{task_id}", json={"title": "will-fail"})
    assert r4.status_code == 404
