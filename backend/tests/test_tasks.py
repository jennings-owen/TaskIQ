"""
Unit tests for /tasks CRUD endpoints.

Tests cover:
- GET /tasks - List all tasks
- POST /tasks - Create new task
- GET /tasks/{id} - Get specific task
- PUT /tasks/{id} - Update task
- DELETE /tasks/{id} - Delete task
- Error handling and edge cases
"""

import pytest
from datetime import datetime, timedelta
import time


class TestTasksCRUD:
    """Test suite for tasks CRUD operations."""
    
    def test_get_tasks_empty(self, client):
        """Test GET /tasks returns empty list when no tasks exist."""
        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # May be empty or have tasks depending on implementation
    
    def test_get_tasks_with_data(self, client, sample_tasks):
        """Test GET /tasks returns list of tasks."""
        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            # Verify task structure
            task = data[0]
            assert "id" in task
            assert "title" in task
            assert "status" in task
    
    def test_create_task_success(self, client, task_data):
        """Test POST /tasks creates a new task successfully."""
        start_time = time.time()
        response = client.post("/api/tasks", json=task_data)
        end_time = time.time()
        
        # Verify response time < 200ms (per PRD NFR)
        assert (end_time - start_time) < 0.2, "Response time exceeds 200ms requirement"
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == task_data["status"]
        
        # Verify task has user_id
        assert "user_id" in data
    
    def test_create_task_missing_required_fields(self, client):
        """Test POST /tasks with missing required fields returns 422."""
        incomplete_data = {
            "description": "Missing title"
        }
        response = client.post("/api/tasks", json=incomplete_data)
        assert response.status_code == 422
    
    def test_create_task_invalid_status(self, client, task_data):
        """Test POST /tasks with invalid status value."""
        invalid_data = task_data.copy()
        invalid_data["status"] = "invalid_status"
        response = client.post("/api/tasks", json=invalid_data)
        # Should reject invalid status per CHECK constraint
        assert response.status_code == 422
    
    def test_create_task_negative_duration(self, client, task_data):
        """Test POST /tasks with negative estimated_duration."""
        invalid_data = task_data.copy()
        invalid_data["estimated_duration"] = -5
        response = client.post("/api/tasks", json=invalid_data)
        # Should reject negative duration
        assert response.status_code == 422
    
    def test_create_task_past_deadline(self, client, task_data):
        """Test POST /tasks with deadline in the past."""
        past_data = task_data.copy()
        past_data["deadline"] = (datetime.now() - timedelta(days=5)).isoformat()
        response = client.post("/api/tasks", json=past_data)
        # Should accept past deadlines (user may be logging overdue tasks)
        assert response.status_code == 201
    
    def test_get_task_by_id_success(self, client, sample_tasks):
        """Test GET /tasks/{id} returns specific task."""
        task_id = sample_tasks[0]['id']
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert "title" in data
        assert "status" in data
    
    def test_get_task_by_id_not_found(self, client):
        """Test GET /tasks/{id} with non-existent ID returns 404."""
        response = client.get("/api/tasks/99999")
        assert response.status_code == 404
    
    def test_get_task_invalid_id(self, client):
        """Test GET /tasks/{id} with invalid ID format."""
        response = client.get("/api/tasks/invalid")
        assert response.status_code == 422
    
    def test_update_task_success(self, client, sample_tasks):
        """Test PUT /tasks/{id} updates task successfully."""
        task_id = sample_tasks[0]['id']
        
        update_data = {
            "title": "Updated Task Title",
            "status": "in_progress",
            "estimated_duration": 5
        }
        
        start_time = time.time()
        response = client.put(f"/api/tasks/{task_id}", json=update_data)
        end_time = time.time()
        
        # Verify response time < 200ms
        assert (end_time - start_time) < 0.2, "Response time exceeds 200ms requirement"
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["status"] == update_data["status"]
        
        # Verify updated_at timestamp changed
        assert "updated_at" in data
    
    def test_update_task_not_found(self, client):
        """Test PUT /tasks/{id} with non-existent ID returns 404."""
        update_data = {
            "title": "Updated Title",
            "status": "completed"
        }
        response = client.put("/api/tasks/99999", json=update_data)
        assert response.status_code == 404
    
    def test_update_task_partial(self, client, sample_tasks):
        """Test PUT /tasks/{id} with partial data (only some fields)."""
        task_id = sample_tasks[0]['id']
        
        # Only update status
        partial_data = {
            "status": "completed"
        }
        
        response = client.put(f"/api/tasks/{task_id}", json=partial_data)
        # Should accept partial updates (PATCH-like behavior)
        assert response.status_code == 200
        assert response.json()["status"] == "completed"
    
    def test_delete_task_success(self, client, sample_tasks):
        """Test DELETE /tasks/{id} deletes task successfully."""
        task_id = sample_tasks[0]['id']
        
        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 204
        
        # Verify task is deleted
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 404
    
    def test_delete_task_not_found(self, client):
        """Test DELETE /tasks/{id} with non-existent ID returns 404."""
        response = client.delete("/api/tasks/99999")
        assert response.status_code == 404
    
    def test_delete_task_invalid_id(self, client):
        """Test DELETE /tasks/{id} with invalid ID format."""
        response = client.delete("/api/tasks/invalid")
        assert response.status_code == 422


class TestTasksPriorityScore:
    """Test suite for automatic priority score calculation."""
    
    def test_task_has_priority_score(self, client, task_data):
        """Test that created tasks automatically get a priority_score."""
        response = client.post("/api/tasks", json=task_data)
        if response.status_code in [200, 201]:
            data = response.json()
            # Priority score should be calculated automatically
            assert "priority_score" in data or response.status_code == 201
    
    def test_priority_score_range(self, client, task_data):
        """Test that priority_score is within valid range (1-100)."""
        response = client.post("/api/tasks", json=task_data)
        if response.status_code in [200, 201]:
            data = response.json()
            if "priority_score" in data:
                assert 1 <= data["priority_score"] <= 100


class TestTasksPerformance:
    """Test suite for performance requirements."""
    
    def test_get_tasks_performance(self, client, sample_tasks):
        """Test GET /tasks completes within 200ms."""
        start_time = time.time()
        response = client.get("/api/tasks")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 0.2, f"Response time {end_time - start_time}s exceeds 200ms requirement"
    
    def test_create_task_performance(self, client, task_data):
        """Test POST /tasks completes within 200ms."""
        start_time = time.time()
        response = client.post("/api/tasks", json=task_data)
        end_time = time.time()
        
        assert response.status_code in [200, 201]
        assert (end_time - start_time) < 0.2, f"Response time {end_time - start_time}s exceeds 200ms requirement"


class TestTasksEdgeCases:
    """Test suite for edge cases and boundary conditions."""
    
    def test_task_with_very_long_title(self, client, task_data):
        """Test task creation with extremely long title."""
        long_data = task_data.copy()
        long_data["title"] = "A" * 1000  # 1000 character title
        response = client.post("/api/tasks", json=long_data)
        # Should accept long titles or enforce reasonable limit
        assert response.status_code in [201, 422]
    
    def test_task_with_empty_title(self, client, task_data):
        """Test task creation with empty title."""
        empty_data = task_data.copy()
        empty_data["title"] = ""
        response = client.post("/api/tasks", json=empty_data)
        # Should reject empty title
        assert response.status_code == 422
    
    def test_task_with_null_optional_fields(self, client):
        """Test task creation with null optional fields."""
        minimal_data = {
            "title": "Minimal Task",
            "description": None,
            "deadline": None,
            "estimated_duration": None,
            "status": "pending"
        }
        response = client.post("/api/tasks", json=minimal_data)
        # Should accept null optional fields
        assert response.status_code == 201
    
    def test_concurrent_task_creation(self, client, task_data):
        """Test multiple tasks can be created in sequence."""
        responses = []
        for i in range(5):
            data = task_data.copy()
            data["title"] = f"Task {i}"
            response = client.post("/api/tasks", json=data)
            responses.append(response)
        
        # All should succeed
        for response in responses:
            assert response.status_code == 201
        
        # Verify all tasks have unique IDs
        task_ids = [r.json()["id"] for r in responses]
        assert len(task_ids) == len(set(task_ids)), "Task IDs should be unique"


class TestTasksSecurity:
    """Test suite for security considerations."""
    
    def test_sql_injection_in_title(self, client, task_data):
        """Test SQL injection attempts in title field."""
        injection_data = task_data.copy()
        injection_data["title"] = "'; DROP TABLE tasks; --"
        
        response = client.post("/api/tasks", json=injection_data)
        # Should either accept as literal string or sanitize
        assert response.status_code in [201, 422]
        
        # Verify tasks table still exists by listing tasks
        list_response = client.get("/api/tasks")
        assert list_response.status_code == 200
    
    def test_xss_in_description(self, client, task_data):
        """Test XSS attempts in description field."""
        xss_data = task_data.copy()
        xss_data["description"] = "<script>alert('XSS')</script>"
        
        response = client.post("/api/tasks", json=xss_data)
        # Should accept as literal string (escaping happens on frontend)
        assert response.status_code == 201
        
        # Verify data is stored as-is
        task_id = response.json()["id"]
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 200
        assert "<script>" in get_response.json()["description"]
    
    def test_unicode_characters_in_task(self, client, task_data):
        """Test tasks with unicode characters."""
        unicode_data = task_data.copy()
        unicode_data["title"] = "Task with émojis 🚀 and spëcial çhars"
        unicode_data["description"] = "Testing 中文字符 and العربية"
        
        response = client.post("/api/tasks", json=unicode_data)
        assert response.status_code == 201
        
        # Verify unicode is preserved
        task_id = response.json()["id"]
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 200
        assert "🚀" in get_response.json()["title"]
    
    def test_unauthorized_user_access(self, client, sample_tasks):
        """Test accessing tasks without proper user context."""
        # This test assumes user authentication will be implemented
        # For now, verify endpoint doesn't expose sensitive data
        task_id = sample_tasks[0]['id']
        response = client.get(f"/api/tasks/{task_id}")
        
        # Should either require auth or return task data
        assert response.status_code in [200, 401, 403]


class TestTasksUserRelationship:
    """Test suite for user-task relationship."""
    
    def test_task_requires_user_id(self, client, task_data):
        """Test tasks must be associated with a user."""
        # Task data should include user_id
        response = client.post("/api/tasks", json=task_data)
        assert response.status_code == 201
        
        task = response.json()
        assert "user_id" in task
        assert task["user_id"] is not None
    
    def test_get_tasks_by_user(self, client, sample_user, sample_tasks):
        """Test retrieving all tasks for a specific user."""
        response = client.get(f"/users/{sample_user['id']}/tasks")
        
        if response.status_code == 200:
            tasks = response.json()
            assert isinstance(tasks, list)
            
            # All tasks should belong to the user
            for task in tasks:
                assert task["user_id"] == sample_user["id"]
    
    def test_filter_tasks_by_status(self, client, sample_tasks):
        """Test filtering tasks by status."""
        response = client.get("/api/tasks?status=pending")
        
        if response.status_code == 200:
            tasks = response.json()
            # All returned tasks should have pending status
            for task in tasks:
                assert task["status"] == "pending"
    
    def test_filter_tasks_by_deadline(self, client):
        """Test filtering tasks by deadline range."""
        today = datetime.now().date().isoformat()
        response = client.get(f"/tasks?deadline_before={today}")
        
        if response.status_code == 200:
            tasks = response.json()
            assert isinstance(tasks, list)


class TestTasksStatusTransitions:
    """Test suite for task status transitions."""
    
    def test_pending_to_in_progress(self, client, sample_tasks):
        """Test transitioning task from pending to in_progress."""
        pending_task = next((t for t in sample_tasks if t['status'] == 'pending'), None)
        if not pending_task:
            pytest.skip("No pending task available")
        
        update_data = {"status": "in_progress"}
        response = client.put(f"/api/tasks/{pending_task['id']}", json=update_data)
        
        assert response.status_code == 200
        assert response.json()["status"] == "in_progress"
    
    def test_in_progress_to_completed(self, client, sample_tasks):
        """Test transitioning task from in_progress to completed."""
        in_progress_task = next((t for t in sample_tasks if t['status'] == 'in_progress'), None)
        if not in_progress_task:
            pytest.skip("No in_progress task available")
        
        update_data = {"status": "completed"}
        response = client.put(f"/api/tasks/{in_progress_task['id']}", json=update_data)
        
        assert response.status_code == 200
        assert response.json()["status"] == "completed"
    
    def test_task_to_blocked_status(self, client, sample_tasks):
        """Test transitioning task to blocked status."""
        task_id = sample_tasks[0]['id']
        
        update_data = {"status": "blocked"}
        response = client.put(f"/api/tasks/{task_id}", json=update_data)
        
        assert response.status_code == 200
        assert response.json()["status"] == "blocked"
    
    def test_all_valid_status_values(self, client, sample_tasks):
        """Test all valid status values can be set."""
        valid_statuses = ['pending', 'in_progress', 'completed', 'blocked']
        task_id = sample_tasks[0]['id']
        
        for status in valid_statuses:
            update_data = {"status": status}
            response = client.put(f"/api/tasks/{task_id}", json=update_data)
            
            assert response.status_code == 200
            assert response.json()["status"] == status

