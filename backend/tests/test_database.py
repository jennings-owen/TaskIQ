"""
Database constraint and integrity tests.

Tests cover:
- Foreign key constraints across all tables
- CASCADE DELETE behavior
- UNIQUE constraints
- CHECK constraints
- Timestamp auto-generation
- Referential integrity
- Database schema validation
"""

import pytest
import sqlite3
from datetime import datetime, timedelta


class TestDatabaseSchema:
    """Test suite for database schema validation."""
    
    def test_users_table_exists(self, test_db):
        """Test users table exists with correct structure."""
        cursor = test_db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        assert cursor.fetchone() is not None
    
    def test_tasks_table_exists(self, test_db):
        """Test tasks table exists with correct structure."""
        cursor = test_db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
        assert cursor.fetchone() is not None
    
    def test_task_dependencies_table_exists(self, test_db):
        """Test task_dependencies table exists."""
        cursor = test_db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='task_dependencies'")
        assert cursor.fetchone() is not None
    
    def test_task_priority_scores_table_exists(self, test_db):
        """Test task_priority_scores table exists."""
        cursor = test_db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='task_priority_scores'")
        assert cursor.fetchone() is not None
    
    def test_task_tshirt_scores_table_exists(self, test_db):
        """Test task_tshirt_scores table exists."""
        cursor = test_db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='task_tshirt_scores'")
        assert cursor.fetchone() is not None


class TestForeignKeyConstraints:
    """Test suite for foreign key constraint enforcement."""
    
    def test_task_requires_valid_user_id(self, test_db, sample_user):
        """Test tasks must reference valid user_id."""
        cursor = test_db.cursor()
        
        # Try to create task with non-existent user_id
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO tasks (user_id, title, status)
                VALUES (?, ?, ?)
            """, (99999, "Invalid User Task", "pending"))
            test_db.commit()
    
    def test_task_dependency_requires_valid_task_ids(self, test_db, sample_tasks):
        """Test task_dependencies must reference valid task IDs."""
        cursor = test_db.cursor()
        
        # Try to create dependency with non-existent task_id
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO task_dependencies (task_id, depends_on_task_id)
                VALUES (?, ?)
            """, (99999, sample_tasks[0]['id']))
            test_db.commit()
    
    def test_priority_score_requires_valid_task_id(self, test_db, sample_tasks):
        """Test task_priority_scores must reference valid task_id."""
        cursor = test_db.cursor()
        
        # Try to create priority score with non-existent task_id
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO task_priority_scores (task_id, score)
                VALUES (?, ?)
            """, (99999, 75))
            test_db.commit()
    
    def test_tshirt_score_requires_valid_task_id(self, test_db, sample_tasks):
        """Test task_tshirt_scores must reference valid task_id."""
        cursor = test_db.cursor()
        
        # Try to create t-shirt score with non-existent task_id
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO task_tshirt_scores (task_id, tshirt_size)
                VALUES (?, ?)
            """, (99999, "M"))
            test_db.commit()


class TestCascadeDelete:
    """Test suite for CASCADE DELETE behavior."""
    
    def test_delete_user_cascades_to_tasks(self, test_db, sample_user, sample_tasks):
        """Test deleting user cascades to delete all their tasks."""
        cursor = test_db.cursor()
        
        # Verify tasks exist
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?", (sample_user['id'],))
        initial_count = cursor.fetchone()[0]
        assert initial_count > 0
        
        # Delete user
        cursor.execute("DELETE FROM users WHERE id = ?", (sample_user['id'],))
        test_db.commit()
        
        # Verify tasks are deleted
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?", (sample_user['id'],))
        final_count = cursor.fetchone()[0]
        assert final_count == 0
    
    def test_delete_task_cascades_to_dependencies(self, test_db, sample_tasks):
        """Test deleting task cascades to delete its dependencies."""
        cursor = test_db.cursor()
        
        # Create dependency
        cursor.execute("""
            INSERT INTO task_dependencies (task_id, depends_on_task_id)
            VALUES (?, ?)
        """, (sample_tasks[0]['id'], sample_tasks[1]['id']))
        test_db.commit()
        
        # Verify dependency exists
        cursor.execute("SELECT COUNT(*) FROM task_dependencies WHERE task_id = ?", 
                      (sample_tasks[0]['id'],))
        assert cursor.fetchone()[0] == 1
        
        # Delete task
        cursor.execute("DELETE FROM tasks WHERE id = ?", (sample_tasks[0]['id'],))
        test_db.commit()
        
        # Verify dependency is deleted
        cursor.execute("SELECT COUNT(*) FROM task_dependencies WHERE task_id = ?", 
                      (sample_tasks[0]['id'],))
        assert cursor.fetchone()[0] == 0
    
    def test_delete_task_cascades_to_priority_scores(self, test_db, sample_tasks):
        """Test deleting task cascades to delete its priority score."""
        cursor = test_db.cursor()
        
        # Create priority score
        cursor.execute("""
            INSERT INTO task_priority_scores (task_id, score, algorithm_version)
            VALUES (?, ?, ?)
        """, (sample_tasks[0]['id'], 85, "v1.0-rulebased"))
        test_db.commit()
        
        # Verify score exists
        cursor.execute("SELECT COUNT(*) FROM task_priority_scores WHERE task_id = ?", 
                      (sample_tasks[0]['id'],))
        assert cursor.fetchone()[0] == 1
        
        # Delete task
        cursor.execute("DELETE FROM tasks WHERE id = ?", (sample_tasks[0]['id'],))
        test_db.commit()
        
        # Verify score is deleted
        cursor.execute("SELECT COUNT(*) FROM task_priority_scores WHERE task_id = ?", 
                      (sample_tasks[0]['id'],))
        assert cursor.fetchone()[0] == 0
    
    def test_delete_task_cascades_to_tshirt_scores(self, test_db, sample_tasks):
        """Test deleting task cascades to delete its t-shirt score."""
        cursor = test_db.cursor()
        
        # Create t-shirt score
        cursor.execute("""
            INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale, algorithm_version)
            VALUES (?, ?, ?, ?)
        """, (sample_tasks[0]['id'], "M", "Medium complexity task", "v1.0"))
        test_db.commit()
        
        # Verify score exists
        cursor.execute("SELECT COUNT(*) FROM task_tshirt_scores WHERE task_id = ?", 
                      (sample_tasks[0]['id'],))
        assert cursor.fetchone()[0] == 1
        
        # Delete task
        cursor.execute("DELETE FROM tasks WHERE id = ?", (sample_tasks[0]['id'],))
        test_db.commit()
        
        # Verify score is deleted
        cursor.execute("SELECT COUNT(*) FROM task_tshirt_scores WHERE task_id = ?", 
                      (sample_tasks[0]['id'],))
        assert cursor.fetchone()[0] == 0
    
    def test_delete_dependency_source_task(self, test_db, sample_tasks):
        """Test deleting source task in dependency relationship."""
        cursor = test_db.cursor()
        
        # Create dependency: task[0] depends on task[1]
        cursor.execute("""
            INSERT INTO task_dependencies (task_id, depends_on_task_id)
            VALUES (?, ?)
        """, (sample_tasks[0]['id'], sample_tasks[1]['id']))
        test_db.commit()
        
        # Delete the task that depends on another
        cursor.execute("DELETE FROM tasks WHERE id = ?", (sample_tasks[0]['id'],))
        test_db.commit()
        
        # Verify dependency is deleted
        cursor.execute("SELECT COUNT(*) FROM task_dependencies WHERE task_id = ?", 
                      (sample_tasks[0]['id'],))
        assert cursor.fetchone()[0] == 0
        
        # Verify the depended-on task still exists
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE id = ?", (sample_tasks[1]['id'],))
        assert cursor.fetchone()[0] == 1
    
    def test_delete_dependency_target_task(self, test_db, sample_tasks):
        """Test deleting target task in dependency relationship."""
        cursor = test_db.cursor()
        
        # Create dependency: task[0] depends on task[1]
        cursor.execute("""
            INSERT INTO task_dependencies (task_id, depends_on_task_id)
            VALUES (?, ?)
        """, (sample_tasks[0]['id'], sample_tasks[1]['id']))
        test_db.commit()
        
        # Delete the task that is depended upon
        cursor.execute("DELETE FROM tasks WHERE id = ?", (sample_tasks[1]['id'],))
        test_db.commit()
        
        # Verify dependency is deleted
        cursor.execute("SELECT COUNT(*) FROM task_dependencies WHERE depends_on_task_id = ?", 
                      (sample_tasks[1]['id'],))
        assert cursor.fetchone()[0] == 0


class TestUniqueConstraints:
    """Test suite for UNIQUE constraint enforcement."""
    
    def test_user_email_must_be_unique(self, test_db, sample_user):
        """Test user email addresses must be unique."""
        cursor = test_db.cursor()
        
        # Try to create another user with same email
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO users (name, email)
                VALUES (?, ?)
            """, ("Another User", sample_user['email']))
            test_db.commit()
    
    def test_task_priority_score_unique_per_task(self, test_db, sample_tasks):
        """Test only one priority score per task."""
        cursor = test_db.cursor()
        
        # Create first priority score
        cursor.execute("""
            INSERT INTO task_priority_scores (task_id, score)
            VALUES (?, ?)
        """, (sample_tasks[0]['id'], 85))
        test_db.commit()
        
        # Try to create second priority score for same task
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO task_priority_scores (task_id, score)
                VALUES (?, ?)
            """, (sample_tasks[0]['id'], 90))
            test_db.commit()
    
    def test_task_tshirt_score_unique_per_task(self, test_db, sample_tasks):
        """Test only one t-shirt score per task."""
        cursor = test_db.cursor()
        
        # Create first t-shirt score
        cursor.execute("""
            INSERT INTO task_tshirt_scores (task_id, tshirt_size)
            VALUES (?, ?)
        """, (sample_tasks[0]['id'], "M"))
        test_db.commit()
        
        # Try to create second t-shirt score for same task
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO task_tshirt_scores (task_id, tshirt_size)
                VALUES (?, ?)
            """, (sample_tasks[0]['id'], "L"))
            test_db.commit()
    
    def test_task_dependency_unique_pair(self, test_db, sample_tasks):
        """Test task dependency pairs must be unique."""
        cursor = test_db.cursor()
        
        # Create first dependency
        cursor.execute("""
            INSERT INTO task_dependencies (task_id, depends_on_task_id)
            VALUES (?, ?)
        """, (sample_tasks[0]['id'], sample_tasks[1]['id']))
        test_db.commit()
        
        # Try to create duplicate dependency
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO task_dependencies (task_id, depends_on_task_id)
                VALUES (?, ?)
            """, (sample_tasks[0]['id'], sample_tasks[1]['id']))
            test_db.commit()


class TestCheckConstraints:
    """Test suite for CHECK constraint enforcement."""
    
    def test_task_status_valid_values(self, test_db, sample_user):
        """Test task status must be one of valid values."""
        cursor = test_db.cursor()
        
        # Valid statuses should work
        valid_statuses = ['pending', 'in_progress', 'completed', 'blocked']
        for status in valid_statuses:
            cursor.execute("""
                INSERT INTO tasks (user_id, title, status)
                VALUES (?, ?, ?)
            """, (sample_user['id'], f"Task with {status}", status))
            test_db.commit()
        
        # Invalid status should fail
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO tasks (user_id, title, status)
                VALUES (?, ?, ?)
            """, (sample_user['id'], "Invalid Status Task", "invalid_status"))
            test_db.commit()
    
    def test_priority_score_range_1_to_100(self, test_db, sample_tasks):
        """Test priority score must be between 1 and 100."""
        cursor = test_db.cursor()
        
        # Valid scores
        for score in [1, 50, 100]:
            cursor.execute("""
                INSERT INTO task_priority_scores (task_id, score)
                VALUES (?, ?)
            """, (sample_tasks[0]['id'], score))
            test_db.commit()
            
            # Clean up for next iteration
            cursor.execute("DELETE FROM task_priority_scores WHERE task_id = ?", 
                          (sample_tasks[0]['id'],))
            test_db.commit()
        
        # Score below 1 should fail
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO task_priority_scores (task_id, score)
                VALUES (?, ?)
            """, (sample_tasks[0]['id'], 0))
            test_db.commit()
        
        # Score above 100 should fail
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO task_priority_scores (task_id, score)
                VALUES (?, ?)
            """, (sample_tasks[1]['id'], 101))
            test_db.commit()
    
    def test_tshirt_size_valid_values(self, test_db, sample_tasks):
        """Test t-shirt size must be one of valid values."""
        cursor = test_db.cursor()
        
        # Valid sizes should work
        valid_sizes = ['XS', 'S', 'M', 'L', 'XL']
        for i, size in enumerate(valid_sizes):
            cursor.execute("""
                INSERT INTO task_tshirt_scores (task_id, tshirt_size)
                VALUES (?, ?)
            """, (sample_tasks[i % len(sample_tasks)]['id'], size))
            test_db.commit()
        
        # Invalid size should fail
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO task_tshirt_scores (task_id, tshirt_size)
                VALUES (?, ?)
            """, (sample_tasks[2]['id'], "XXL"))
            test_db.commit()


class TestTimestampGeneration:
    """Test suite for automatic timestamp generation."""
    
    def test_user_created_at_auto_generated(self, test_db):
        """Test user created_at is automatically set."""
        cursor = test_db.cursor()
        
        cursor.execute("""
            INSERT INTO users (name, email)
            VALUES (?, ?)
        """, ("Test User", "timestamp@test.com"))
        test_db.commit()
        
        cursor.execute("SELECT created_at FROM users WHERE email = ?", ("timestamp@test.com",))
        created_at = cursor.fetchone()[0]
        
        assert created_at is not None
        assert len(created_at) > 0
    
    def test_task_created_at_auto_generated(self, test_db, sample_user):
        """Test task created_at is automatically set."""
        cursor = test_db.cursor()
        
        cursor.execute("""
            INSERT INTO tasks (user_id, title, status)
            VALUES (?, ?, ?)
        """, (sample_user['id'], "Timestamp Test Task", "pending"))
        test_db.commit()
        
        task_id = cursor.lastrowid
        cursor.execute("SELECT created_at FROM tasks WHERE id = ?", (task_id,))
        created_at = cursor.fetchone()[0]
        
        assert created_at is not None
        assert len(created_at) > 0
    
    def test_task_updated_at_auto_generated(self, test_db, sample_user):
        """Test task updated_at is automatically set."""
        cursor = test_db.cursor()
        
        cursor.execute("""
            INSERT INTO tasks (user_id, title, status)
            VALUES (?, ?, ?)
        """, (sample_user['id'], "Update Test Task", "pending"))
        test_db.commit()
        
        task_id = cursor.lastrowid
        cursor.execute("SELECT updated_at FROM tasks WHERE id = ?", (task_id,))
        updated_at = cursor.fetchone()[0]
        
        assert updated_at is not None
        assert len(updated_at) > 0
    
    def test_priority_score_generated_at_auto_generated(self, test_db, sample_tasks):
        """Test priority score generated_at is automatically set."""
        cursor = test_db.cursor()
        
        cursor.execute("""
            INSERT INTO task_priority_scores (task_id, score)
            VALUES (?, ?)
        """, (sample_tasks[0]['id'], 75))
        test_db.commit()
        
        cursor.execute("SELECT generated_at FROM task_priority_scores WHERE task_id = ?", 
                      (sample_tasks[0]['id'],))
        generated_at = cursor.fetchone()[0]
        
        assert generated_at is not None
        assert len(generated_at) > 0
    
    def test_tshirt_score_generated_at_auto_generated(self, test_db, sample_tasks):
        """Test t-shirt score generated_at is automatically set."""
        cursor = test_db.cursor()
        
        cursor.execute("""
            INSERT INTO task_tshirt_scores (task_id, tshirt_size)
            VALUES (?, ?)
        """, (sample_tasks[0]['id'], "M"))
        test_db.commit()
        
        cursor.execute("SELECT generated_at FROM task_tshirt_scores WHERE task_id = ?", 
                      (sample_tasks[0]['id'],))
        generated_at = cursor.fetchone()[0]
        
        assert generated_at is not None
        assert len(generated_at) > 0


class TestReferentialIntegrity:
    """Test suite for referential integrity across tables."""
    
    def test_task_user_relationship(self, test_db, sample_user, sample_tasks):
        """Test tasks correctly reference their owner user."""
        cursor = test_db.cursor()
        
        for task in sample_tasks:
            cursor.execute("SELECT user_id FROM tasks WHERE id = ?", (task['id'],))
            user_id = cursor.fetchone()[0]
            assert user_id == sample_user['id']
    
    def test_priority_score_task_relationship(self, test_db, sample_tasks):
        """Test priority scores correctly reference tasks."""
        cursor = test_db.cursor()
        
        # Create priority score
        cursor.execute("""
            INSERT INTO task_priority_scores (task_id, score)
            VALUES (?, ?)
        """, (sample_tasks[0]['id'], 85))
        test_db.commit()
        
        # Verify relationship
        cursor.execute("""
            SELECT t.id, t.title, ps.score
            FROM tasks t
            JOIN task_priority_scores ps ON t.id = ps.task_id
            WHERE t.id = ?
        """, (sample_tasks[0]['id'],))
        
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == sample_tasks[0]['id']
        assert result[2] == 85
    
    def test_tshirt_score_task_relationship(self, test_db, sample_tasks):
        """Test t-shirt scores correctly reference tasks."""
        cursor = test_db.cursor()
        
        # Create t-shirt score
        cursor.execute("""
            INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale)
            VALUES (?, ?, ?)
        """, (sample_tasks[0]['id'], "L", "Large complexity"))
        test_db.commit()
        
        # Verify relationship
        cursor.execute("""
            SELECT t.id, t.title, ts.tshirt_size, ts.rationale
            FROM tasks t
            JOIN task_tshirt_scores ts ON t.id = ts.task_id
            WHERE t.id = ?
        """, (sample_tasks[0]['id'],))
        
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == sample_tasks[0]['id']
        assert result[2] == "L"
        assert result[3] == "Large complexity"
    
    def test_task_dependency_relationship(self, test_db, sample_tasks):
        """Test task dependencies correctly reference both tasks."""
        cursor = test_db.cursor()
        
        # Create dependency
        cursor.execute("""
            INSERT INTO task_dependencies (task_id, depends_on_task_id)
            VALUES (?, ?)
        """, (sample_tasks[0]['id'], sample_tasks[1]['id']))
        test_db.commit()
        
        # Verify relationship
        cursor.execute("""
            SELECT t1.title as task_title, t2.title as depends_on_title
            FROM task_dependencies td
            JOIN tasks t1 ON td.task_id = t1.id
            JOIN tasks t2 ON td.depends_on_task_id = t2.id
            WHERE td.task_id = ?
        """, (sample_tasks[0]['id'],))
        
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == sample_tasks[0]['title']
        assert result[1] == sample_tasks[1]['title']
    
    def test_orphaned_priority_scores_prevented(self, test_db, sample_tasks):
        """Test priority scores cannot exist without parent task."""
        cursor = test_db.cursor()
        
        # Create priority score
        cursor.execute("""
            INSERT INTO task_priority_scores (task_id, score)
            VALUES (?, ?)
        """, (sample_tasks[0]['id'], 85))
        test_db.commit()
        
        # Delete task (should cascade delete priority score)
        cursor.execute("DELETE FROM tasks WHERE id = ?", (sample_tasks[0]['id'],))
        test_db.commit()
        
        # Verify no orphaned priority scores
        cursor.execute("SELECT COUNT(*) FROM task_priority_scores WHERE task_id = ?", 
                      (sample_tasks[0]['id'],))
        assert cursor.fetchone()[0] == 0


