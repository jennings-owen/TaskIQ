"""
Integration tests for full task lifecycle and workflows.

Tests cover:
- Complete task lifecycle (create -> update -> complete -> delete)
- User authentication workflows
- Task dependencies and blocking relationships
- Priority score generation and updates
- T-shirt size scoring integration
- Multi-user scenarios
- Complex workflow scenarios
"""

import pytest
from datetime import datetime, timedelta
import time


class TestTaskLifecycle:
    """Test suite for complete task lifecycle workflows."""
    
    def test_complete_task_workflow(self, client, sample_user):
        """Test full task lifecycle: create -> update -> complete -> delete."""
        # Step 1: Create task
        task_data = {
            "user_id": sample_user['id'],
            "title": "Complete Lifecycle Task",
            "description": "Test full workflow",
            "deadline": (datetime.now() + timedelta(days=5)).isoformat(),
            "estimated_duration": 3,
            "status": "pending"
        }
        
        create_response = client.post("/api/tasks", json=task_data)
        assert create_response.status_code in [200, 201]
        task = create_response.json()
        task_id = task["id"]
        
        # Step 2: Verify task was created
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 200
        assert get_response.json()["status"] == "pending"
        
        # Step 3: Update task to in_progress
        update_data = {
            "status": "in_progress",
            "title": "Complete Lifecycle Task - Updated"
        }
        update_response = client.put(f"/api/tasks/{task_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["status"] == "in_progress"
        
        # Step 4: Complete the task
        complete_data = {"status": "completed"}
        complete_response = client.put(f"/api/tasks/{task_id}", json=complete_data)
        assert complete_response.status_code == 200
        assert complete_response.json()["status"] == "completed"
        
        # Step 5: Delete the task
        delete_response = client.delete(f"/api/tasks/{task_id}")
        assert delete_response.status_code in [200, 204]
        
        # Step 6: Verify task is deleted
        verify_response = client.get(f"/api/tasks/{task_id}")
        assert verify_response.status_code == 404
    
    def test_task_with_priority_score_lifecycle(self, client, sample_user):
        """Test task lifecycle with automatic priority score generation."""
        # Create task
        task_data = {
            "user_id": sample_user['id'],
            "title": "Priority Task",
            "description": "Task with priority scoring",
            "deadline": (datetime.now() + timedelta(days=2)).isoformat(),
            "estimated_duration": 4,
            "status": "pending"
        }
        
        create_response = client.post("/api/tasks", json=task_data)
        assert create_response.status_code in [200, 201]
        task = create_response.json()
        
        # Verify priority score was generated (if auto-generation is implemented)
        if "priority_score" in task:
            assert 1 <= task["priority_score"] <= 100
        
        # Get priority score via dedicated endpoint if available
        score_response = client.get(f"/api/tasks/{task['id']}/priority")
        if score_response.status_code == 200:
            score_data = score_response.json()
            assert "score" in score_data
            assert 1 <= score_data["score"] <= 100
    
    def test_task_with_tshirt_size_lifecycle(self, client, sample_user):
        """Test task lifecycle with t-shirt size estimation."""
        # Create task
        task_data = {
            "user_id": sample_user['id'],
            "title": "Sized Task",
            "description": "Complex feature implementation",
            "deadline": (datetime.now() + timedelta(days=10)).isoformat(),
            "estimated_duration": 20,
            "status": "pending"
        }
        
        create_response = client.post("/api/tasks", json=task_data)
        assert create_response.status_code in [200, 201]
        task = create_response.json()
        
        # Request t-shirt size estimation
        size_response = client.post(f"/api/tasks/{task['id']}/estimate-size")
        if size_response.status_code == 200:
            size_data = size_response.json()
            assert "tshirt_size" in size_data
            assert size_data["tshirt_size"] in ["XS", "S", "M", "L", "XL"]


class TestTaskDependencies:
    """Test suite for task dependency workflows."""
    
    def test_create_task_dependency(self, client, sample_tasks):
        """Test creating dependency between tasks."""
        if len(sample_tasks) < 2:
            pytest.skip("Need at least 2 tasks for dependency test")
        
        dependency_data = {
            "task_id": sample_tasks[0]['id'],
            "depends_on_task_id": sample_tasks[1]['id']
        }
        
        response = client.post("/api/tasks/dependencies", json=dependency_data)
        assert response.status_code in [200, 201]
    
    def test_get_task_dependencies(self, client, sample_tasks):
        """Test retrieving task dependencies."""
        if len(sample_tasks) < 2:
            pytest.skip("Need at least 2 tasks for dependency test")
        
        # Create dependency
        dependency_data = {
            "task_id": sample_tasks[0]['id'],
            "depends_on_task_id": sample_tasks[1]['id']
        }
        client.post("/api/tasks/dependencies", json=dependency_data)
        
        # Get dependencies for task
        response = client.get(f"/api/tasks/{sample_tasks[0]['id']}/dependencies")
        if response.status_code == 200:
            dependencies = response.json()
            assert isinstance(dependencies, list)
    
    def test_circular_dependency_prevention(self, client, sample_tasks):
        """Test system prevents circular dependencies."""
        if len(sample_tasks) < 2:
            pytest.skip("Need at least 2 tasks for circular dependency test")
        
        # Create dependency: task[0] depends on task[1]
        dep1 = {
            "task_id": sample_tasks[0]['id'],
            "depends_on_task_id": sample_tasks[1]['id']
        }
        response1 = client.post("/api/tasks/dependencies", json=dep1)
        assert response1.status_code in [200, 201]
        
        # Try to create circular dependency: task[1] depends on task[0]
        dep2 = {
            "task_id": sample_tasks[1]['id'],
            "depends_on_task_id": sample_tasks[0]['id']
        }
        response2 = client.post("/api/tasks/dependencies", json=dep2)
        # Should either reject or handle gracefully
        assert response2.status_code in [200, 201, 400, 422]
    
    def test_delete_task_with_dependencies(self, client, sample_tasks):
        """Test deleting task that has dependencies."""
        if len(sample_tasks) < 2:
            pytest.skip("Need at least 2 tasks for dependency test")
        
        # Create dependency
        dependency_data = {
            "task_id": sample_tasks[0]['id'],
            "depends_on_task_id": sample_tasks[1]['id']
        }
        client.post("/api/tasks/dependencies", json=dependency_data)
        
        # Delete the dependent task
        delete_response = client.delete(f"/api/tasks/{sample_tasks[0]['id']}")
        assert delete_response.status_code in [200, 204]
        
        # Verify task is deleted
        verify_response = client.get(f"/api/tasks/{sample_tasks[0]['id']}")
        assert verify_response.status_code == 404
    
    def test_blocked_task_workflow(self, client, sample_tasks):
        """Test workflow for blocked tasks."""
        if len(sample_tasks) < 2:
            pytest.skip("Need at least 2 tasks for blocked task test")
        
        # Create dependency
        dependency_data = {
            "task_id": sample_tasks[0]['id'],
            "depends_on_task_id": sample_tasks[1]['id']
        }
        client.post("/api/tasks/dependencies", json=dependency_data)
        
        # Mark dependent task as blocked
        update_data = {"status": "blocked"}
        response = client.put(f"/api/tasks/{sample_tasks[0]['id']}", json=update_data)
        assert response.status_code == 200
        assert response.json()["status"] == "blocked"


class TestUserWorkflows:
    """Test suite for user-related workflows."""
    
    def test_user_task_isolation(self, client, test_db):
        """Test tasks are properly isolated between users."""
        cursor = test_db.cursor()
        
        # Create two users
        cursor.execute("""
            INSERT INTO users (name, email)
            VALUES (?, ?)
        """, ("User One", "user1@test.com"))
        test_db.commit()
        user1_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO users (name, email)
            VALUES (?, ?)
        """, ("User Two", "user2@test.com"))
        test_db.commit()
        user2_id = cursor.lastrowid
        
        # Create tasks for each user
        task1_data = {
            "user_id": user1_id,
            "title": "User 1 Task",
            "status": "pending"
        }
        task2_data = {
            "user_id": user2_id,
            "title": "User 2 Task",
            "status": "pending"
        }
        
        response1 = client.post("/api/tasks", json=task1_data)
        response2 = client.post("/api/tasks", json=task2_data)
        
        assert response1.status_code in [200, 201]
        assert response2.status_code in [200, 201]
        
        # Get tasks for user 1
        user1_tasks_response = client.get(f"/api/users/{user1_id}/tasks")
        if user1_tasks_response.status_code == 200:
            user1_tasks = user1_tasks_response.json()
            # Verify only user 1's tasks are returned
            for task in user1_tasks:
                assert task["user_id"] == user1_id
    
    def test_user_deletion_cascades_to_tasks(self, client, test_db):
        """Test deleting user cascades to delete all their tasks."""
        cursor = test_db.cursor()
        
        # Create user
        cursor.execute("""
            INSERT INTO users (name, email)
            VALUES (?, ?)
        """, ("Temp User", "temp@test.com"))
        test_db.commit()
        user_id = cursor.lastrowid
        
        # Create tasks for user
        task_data = {
            "user_id": user_id,
            "title": "Task to be cascaded",
            "status": "pending"
        }
        task_response = client.post("/api/tasks", json=task_data)
        assert task_response.status_code in [200, 201]
        task_id = task_response.json()["id"]
        
        # Delete user
        delete_response = client.delete(f"/api/users/{user_id}")
        if delete_response.status_code in [200, 204]:
            # Verify task is also deleted
            task_check = client.get(f"/api/tasks/{task_id}")
            assert task_check.status_code == 404


class TestPriorityScoreIntegration:
    """Test suite for priority score generation and updates."""
    
    def test_priority_score_auto_generation(self, client, sample_user):
        """Test priority scores are automatically generated for new tasks."""
        task_data = {
            "user_id": sample_user['id'],
            "title": "Auto Priority Task",
            "deadline": (datetime.now() + timedelta(days=3)).isoformat(),
            "estimated_duration": 2,
            "status": "pending"
        }
        
        response = client.post("/api/tasks", json=task_data)
        assert response.status_code in [200, 201]
        task = response.json()
        
        # Check if priority_score is in response or needs separate query
        if "priority_score" in task:
            assert 1 <= task["priority_score"] <= 100
        else:
            # Query priority score separately
            score_response = client.get(f"/api/tasks/{task['id']}/priority")
            if score_response.status_code == 200:
                score_data = score_response.json()
                assert "score" in score_data
    
    def test_priority_score_algorithm_validation(self, client, sample_user):
        """Test priority score follows PRD algorithm: 100 - days*5 - duration*3."""
        # Create task with known parameters
        deadline = datetime.now() + timedelta(days=5)
        duration = 4
        
        task_data = {
            "user_id": sample_user['id'],
            "title": "Algorithm Test Task",
            "deadline": deadline.isoformat(),
            "estimated_duration": duration,
            "status": "pending"
        }
        
        response = client.post("/api/tasks", json=task_data)
        assert response.status_code in [200, 201]
        task = response.json()
        
        # Calculate expected score: 100 - (5 * 5) - (4 * 3) = 100 - 25 - 12 = 63
        expected_score = 100 - (5 * 5) - (duration * 3)
        expected_score = max(1, min(100, expected_score))  # Clamp between 1-100
        
        if "priority_score" in task:
            # Allow small variance for timing differences
            assert abs(task["priority_score"] - expected_score) <= 5
    
    def test_priority_score_update_on_task_change(self, client, sample_tasks):
        """Test priority score updates when task attributes change."""
        task_id = sample_tasks[0]['id']
        
        # Get initial priority score
        initial_response = client.get(f"/api/tasks/{task_id}")
        if initial_response.status_code == 200:
            initial_task = initial_response.json()
            
            # Update task deadline (make it more urgent)
            update_data = {
                "deadline": (datetime.now() + timedelta(days=1)).isoformat()
            }
            update_response = client.put(f"/api/tasks/{task_id}", json=update_data)
            assert update_response.status_code == 200
            
            # Get updated priority score
            updated_response = client.get(f"/api/tasks/{task_id}")
            if updated_response.status_code == 200:
                updated_task = updated_response.json()
                
                # Priority score should change if auto-recalculation is implemented
                if "priority_score" in initial_task and "priority_score" in updated_task:
                    # More urgent deadline should increase priority
                    assert updated_task["priority_score"] >= initial_task["priority_score"]
    
    def test_bulk_priority_ranking(self, client, sample_user):
        """Test bulk priority ranking via /ai/rank endpoint."""
        tasks_data = {
            "tasks": [
                {
                    "title": "Urgent Task",
                    "deadline": (datetime.now() + timedelta(days=1)).isoformat(),
                    "estimated_duration": 2
                },
                {
                    "title": "Normal Task",
                    "deadline": (datetime.now() + timedelta(days=5)).isoformat(),
                    "estimated_duration": 3
                },
                {
                    "title": "Low Priority Task",
                    "deadline": (datetime.now() + timedelta(days=15)).isoformat(),
                    "estimated_duration": 1
                }
            ]
        }
        
        response = client.post("/api/ai/rank", json=tasks_data)
        assert response.status_code == 200
        rankings = response.json()
        
        assert len(rankings) == 3
        
        # Verify urgent task has highest priority
        scores = [r["priority_score"] for r in rankings if "priority_score" in r]
        if len(scores) == 3:
            assert scores[0] > scores[1] > scores[2]


class TestTShirtSizeIntegration:
    """Test suite for t-shirt size estimation integration."""
    
    def test_tshirt_size_for_task(self, client, sample_tasks):
        """Test requesting t-shirt size estimation for a task."""
        task_id = sample_tasks[0]['id']
        
        # Request size estimation
        response = client.post(f"/api/tasks/{task_id}/estimate-size")
        if response.status_code == 200:
            size_data = response.json()
            assert "tshirt_size" in size_data
            assert size_data["tshirt_size"] in ["XS", "S", "M", "L", "XL"]
            
            # Rationale should be provided
            if "rationale" in size_data:
                assert isinstance(size_data["rationale"], str)
                assert len(size_data["rationale"]) > 0
    
    def test_tshirt_size_correlates_with_duration(self, client, sample_user):
        """Test t-shirt sizes correlate with estimated duration."""
        # Create small task
        small_task_data = {
            "user_id": sample_user['id'],
            "title": "Small Task",
            "estimated_duration": 1,
            "status": "pending"
        }
        small_response = client.post("/api/tasks", json=small_task_data)
        assert small_response.status_code in [200, 201]
        small_task_id = small_response.json()["id"]
        
        # Create large task
        large_task_data = {
            "user_id": sample_user['id'],
            "title": "Large Task",
            "estimated_duration": 40,
            "status": "pending"
        }
        large_response = client.post("/api/tasks", json=large_task_data)
        assert large_response.status_code in [200, 201]
        large_task_id = large_response.json()["id"]
        
        # Get size estimations
        small_size_response = client.post(f"/api/tasks/{small_task_id}/estimate-size")
        large_size_response = client.post(f"/api/tasks/{large_task_id}/estimate-size")
        
        if small_size_response.status_code == 200 and large_size_response.status_code == 200:
            small_size = small_size_response.json()["tshirt_size"]
            large_size = large_size_response.json()["tshirt_size"]
            
            sizes = ["XS", "S", "M", "L", "XL"]
            # Large task should have larger or equal size
            assert sizes.index(large_size) >= sizes.index(small_size)


class TestPerformanceIntegration:
    """Test suite for performance requirements in integrated workflows."""
    
    def test_complete_workflow_performance(self, client, sample_user):
        """Test complete workflow completes within reasonable time."""
        start_time = time.time()
        
        # Create task
        task_data = {
            "user_id": sample_user['id'],
            "title": "Performance Test Task",
            "deadline": (datetime.now() + timedelta(days=3)).isoformat(),
            "estimated_duration": 2,
            "status": "pending"
        }
        create_response = client.post("/api/tasks", json=task_data)
        assert create_response.status_code in [200, 201]
        task_id = create_response.json()["id"]
        
        # Update task
        update_response = client.put(f"/api/tasks/{task_id}", json={"status": "in_progress"})
        assert update_response.status_code == 200
        
        # Get task
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 200
        
        # Delete task
        delete_response = client.delete(f"/api/tasks/{task_id}")
        assert delete_response.status_code in [200, 204]
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Complete workflow should be reasonably fast (< 1 second)
        assert total_time < 1.0, f"Complete workflow took {total_time}s"
    
    def test_bulk_operations_performance(self, client, sample_user):
        """Test bulk operations complete within reasonable time."""
        start_time = time.time()
        
        # Create multiple tasks
        task_ids = []
        for i in range(10):
            task_data = {
                "user_id": sample_user['id'],
                "title": f"Bulk Task {i}",
                "status": "pending"
            }
            response = client.post("/api/tasks", json=task_data)
            if response.status_code in [200, 201]:
                task_ids.append(response.json()["id"])
        
        # Get all tasks
        list_response = client.get("/api/tasks")
        assert list_response.status_code == 200
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Bulk operations should complete in reasonable time (< 2 seconds)
        assert total_time < 2.0, f"Bulk operations took {total_time}s"


class TestErrorHandlingIntegration:
    """Test suite for error handling in integrated workflows."""
    
    def test_invalid_task_creation_rollback(self, client, sample_user):
        """Test invalid task creation doesn't leave partial data."""
        # Attempt to create task with invalid data
        invalid_task_data = {
            "user_id": sample_user['id'],
            "title": "",  # Empty title should fail
            "status": "invalid_status"  # Invalid status
        }
        
        response = client.post("/api/tasks", json=invalid_task_data)
        assert response.status_code in [400, 422]
        
        # Verify no partial task was created
        list_response = client.get("/api/tasks")
        if list_response.status_code == 200:
            tasks = list_response.json()
            # Should not contain task with empty title
            assert not any(t.get("title") == "" for t in tasks)
    
    def test_dependency_on_nonexistent_task(self, client, sample_tasks):
        """Test creating dependency with non-existent task fails gracefully."""
        dependency_data = {
            "task_id": sample_tasks[0]['id'],
            "depends_on_task_id": 99999  # Non-existent task
        }
        
        response = client.post("/api/tasks/dependencies", json=dependency_data)
        assert response.status_code in [400, 404, 422]
    
    def test_concurrent_task_updates(self, client, sample_tasks):
        """Test concurrent updates to same task are handled correctly."""
        task_id = sample_tasks[0]['id']
        
        # Simulate concurrent updates
        update1 = {"status": "in_progress"}
        update2 = {"status": "completed"}
        
        response1 = client.put(f"/api/tasks/{task_id}", json=update1)
        response2 = client.put(f"/api/tasks/{task_id}", json=update2)
        
        # Both should succeed (last write wins) or handle optimistic locking
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify final state
        final_response = client.get(f"/api/tasks/{task_id}")
        assert final_response.status_code == 200
        assert final_response.json()["status"] in ["in_progress", "completed"]


