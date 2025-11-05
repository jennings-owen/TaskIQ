"""
Pytest configuration and fixtures for backend tests.

This module provides test fixtures for database setup, test client,
and sample data for testing the Agile TaskIQ API.
"""

import pytest
from fastapi.testclient import TestClient
import sqlite3
from datetime import datetime, timedelta
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from main import app
except ImportError:
    app = None


# Schema from schema.sql
SCHEMA_SQL = """
-- Table for storing user information
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing tasks assigned to users
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    deadline TEXT,
    estimated_duration INTEGER,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'in_progress', 'completed', 'blocked')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Junction table to manage dependencies between tasks
CREATE TABLE task_dependencies (
    id INTEGER PRIMARY KEY,
    task_id INTEGER NOT NULL,
    depends_on_task_id INTEGER NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (depends_on_task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    UNIQUE(task_id, depends_on_task_id)
);

-- Table to store AI-generated priority scores for tasks
CREATE TABLE task_priority_scores (
    id INTEGER PRIMARY KEY,
    task_id INTEGER NOT NULL UNIQUE,
    score INTEGER NOT NULL CHECK(score >= 1 AND score <= 100),
    algorithm_version TEXT,
    generated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

-- Table to store AI-generated T-shirt size estimations for tasks
CREATE TABLE task_tshirt_scores (
    id INTEGER PRIMARY KEY,
    task_id INTEGER NOT NULL UNIQUE,
    tshirt_size TEXT NOT NULL CHECK(tshirt_size IN ('XS', 'S', 'M', 'L', 'XL')),
    rationale TEXT,
    algorithm_version TEXT,
    generated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);
"""


@pytest.fixture(scope="function")
def test_db():
    """
    Create a fresh test database for each test function.
    Uses SQLite in-memory database with schema.sql structure.
    """
    # Create in-memory database connection
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    
    # Execute schema
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    
    yield conn
    
    # Cleanup
    conn.close()


@pytest.fixture(scope="function")
def integration_db():
    """
    Load or create test.db file for integration testing.
    Auto-generates test.db if it doesn't exist.
    
    Provides a consistent, pre-populated database for full integration tests.
    """
    import os
    import shutil
    
    test_db_path = os.path.join(os.path.dirname(__file__), 'test.db')
    
    # Auto-generate test.db if it doesn't exist
    if not os.path.exists(test_db_path):
        print(f"\nAuto-generating test.db at {test_db_path}...")
        _create_test_database(test_db_path)
    
    # Create a temporary copy for this test
    temp_db_path = os.path.join(os.path.dirname(__file__), 'temp_integration.db')
    shutil.copy2(test_db_path, temp_db_path)
    
    # Connect to the temporary database
    conn = sqlite3.connect(temp_db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    
    yield conn
    
    # Cleanup
    conn.close()
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)


def _create_test_database(db_path):
    """Helper function to create test.db with sample data."""
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA_SQL)
    cursor = conn.cursor()
    
    # Insert sample users
    cursor.execute("INSERT INTO users (id, name, email, password_hash) VALUES (1, 'Alice Johnson', 'alice@example.com', 'hash1')")
    cursor.execute("INSERT INTO users (id, name, email, password_hash) VALUES (2, 'Bob Smith', 'bob@example.com', 'hash2')")
    cursor.execute("INSERT INTO users (id, name, email, password_hash) VALUES (3, 'Carol Williams', 'carol@example.com', 'hash3')")
    
    # Insert sample tasks
    today = datetime.now()
    cursor.execute("INSERT INTO tasks (id, user_id, title, description, deadline, estimated_duration, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (1, 1, 'Fix critical bug', 'Production issue', (today + timedelta(days=1)).isoformat(), 4, 'in_progress'))
    cursor.execute("INSERT INTO tasks (id, user_id, title, description, deadline, estimated_duration, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (2, 1, 'Submit report', 'Q4 metrics', (today + timedelta(days=2)).isoformat(), 6, 'pending'))
    cursor.execute("INSERT INTO tasks (id, user_id, title, description, deadline, estimated_duration, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (3, 2, 'Review audit', 'Security findings', (today + timedelta(days=3)).isoformat(), 5, 'pending'))
    
    # Insert task dependencies
    cursor.execute("INSERT INTO task_dependencies (task_id, depends_on_task_id) VALUES (2, 1)")
    
    # Insert priority scores
    cursor.execute("INSERT INTO task_priority_scores (task_id, score) VALUES (1, 95)")
    cursor.execute("INSERT INTO task_priority_scores (task_id, score) VALUES (2, 88)")
    cursor.execute("INSERT INTO task_priority_scores (task_id, score) VALUES (3, 82)")
    
    # Insert t-shirt scores
    cursor.execute("INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) VALUES (1, 'M', 'Critical bug fix')")
    cursor.execute("INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale) VALUES (2, 'L', 'Comprehensive report')")
    
    conn.commit()
    conn.close()
    print(f"Test database created at {db_path}")


@pytest.fixture(scope="function")
def client(test_db):
    """
    Create a test client with database connection.
    """
    if app is None:
        pytest.skip("FastAPI app not available")
    
    # Store db connection in app state for access in endpoints
    app.state.test_db = test_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Cleanup
    if hasattr(app.state, 'test_db'):
        delattr(app.state, 'test_db')


@pytest.fixture
def sample_user(test_db):
    """
    Create a sample user for testing using direct SQL.
    """
    cursor = test_db.cursor()
    cursor.execute("""
        INSERT INTO users (name, email, password_hash)
        VALUES (?, ?, ?)
    """, ("Test User", "test@example.com", "hashed_password_123"))
    test_db.commit()
    
    user_id = cursor.lastrowid
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = dict(cursor.fetchone())
    
    return user


@pytest.fixture
def sample_tasks(test_db, sample_user):
    """
    Create sample tasks for testing using direct SQL.
    """
    cursor = test_db.cursor()
    
    tasks_data = [
        (
            sample_user['id'],
            "Submit project report",
            "Send final report to manager",
            (datetime.now() + timedelta(days=2)).isoformat(),
            4,
            "pending"
        ),
        (
            sample_user['id'],
            "Clean workspace",
            "Organize desk and files",
            (datetime.now() + timedelta(days=10)).isoformat(),
            1,
            "pending"
        ),
        (
            sample_user['id'],
            "Review code",
            "Review pull requests",
            (datetime.now() + timedelta(days=1)).isoformat(),
            2,
            "in_progress"
        )
    ]
    
    tasks = []
    for task_data in tasks_data:
        cursor.execute("""
            INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, task_data)
        test_db.commit()
        
        task_id = cursor.lastrowid
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        tasks.append(dict(cursor.fetchone()))
    
    return tasks


@pytest.fixture
def task_data():
    """
    Provide sample task data for POST requests.
    """
    return {
        "title": "New Task",
        "description": "Task description",
        "deadline": (datetime.now() + timedelta(days=5)).isoformat(),
        "estimated_duration": 3,
        "status": "pending"
    }


@pytest.fixture
def ai_rank_data():
    """
    Provide sample data for /ai/rank endpoint testing.
    """
    return {
        "tasks": [
            {
                "title": "Submit project report",
                "deadline": (datetime.now() + timedelta(days=2)).isoformat(),
                "estimated_duration": 4
            },
            {
                "title": "Clean workspace",
                "deadline": (datetime.now() + timedelta(days=10)).isoformat(),
                "estimated_duration": 1
            }
        ]
    }


@pytest.fixture
def ai_size_data():
    """
    Provide sample data for /ai/size endpoint testing.
    """
    return {
        "height_cm": 175,
        "weight_kg": 70,
        "gender": "male",
        "fit_preference": "regular"
    }


@pytest.fixture
def multiple_users(test_db):
    """
    Create multiple users for integration testing.
    """
    cursor = test_db.cursor()
    
    users_data = [
        ("Alice Smith", "alice@example.com", "hash123"),
        ("Bob Jones", "bob@example.com", "hash456"),
        ("Charlie Brown", "charlie@example.com", "hash789")
    ]
    
    users = []
    for user_data in users_data:
        cursor.execute("""
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
        """, user_data)
        test_db.commit()
        
        user_id = cursor.lastrowid
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        users.append(dict(cursor.fetchone()))
    
    return users


@pytest.fixture
def tasks_with_dependencies(test_db, sample_user):
    """
    Create tasks with dependency relationships for testing.
    """
    cursor = test_db.cursor()
    
    # Create tasks
    tasks_data = [
        (sample_user['id'], "Design Database", "Create schema", None, 8, "completed"),
        (sample_user['id'], "Implement API", "Build endpoints", None, 16, "in_progress"),
        (sample_user['id'], "Write Tests", "Unit and integration tests", None, 12, "pending"),
        (sample_user['id'], "Deploy Application", "Production deployment", None, 4, "blocked")
    ]
    
    tasks = []
    for task_data in tasks_data:
        cursor.execute("""
            INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, task_data)
        test_db.commit()
        
        task_id = cursor.lastrowid
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        tasks.append(dict(cursor.fetchone()))
    
    # Create dependencies
    # API depends on Database
    cursor.execute("""
        INSERT INTO task_dependencies (task_id, depends_on_task_id)
        VALUES (?, ?)
    """, (tasks[1]['id'], tasks[0]['id']))
    
    # Tests depend on API
    cursor.execute("""
        INSERT INTO task_dependencies (task_id, depends_on_task_id)
        VALUES (?, ?)
    """, (tasks[2]['id'], tasks[1]['id']))
    
    # Deploy depends on Tests
    cursor.execute("""
        INSERT INTO task_dependencies (task_id, depends_on_task_id)
        VALUES (?, ?)
    """, (tasks[3]['id'], tasks[2]['id']))
    
    test_db.commit()
    
    return tasks


@pytest.fixture
def tasks_with_scores(test_db, sample_user):
    """
    Create tasks with priority and t-shirt scores for testing.
    """
    cursor = test_db.cursor()
    
    # Create tasks
    tasks_data = [
        (sample_user['id'], "High Priority Task", "Urgent work", 
         (datetime.now() + timedelta(days=1)).isoformat(), 2, "pending"),
        (sample_user['id'], "Medium Priority Task", "Normal work",
         (datetime.now() + timedelta(days=5)).isoformat(), 4, "pending"),
        (sample_user['id'], "Low Priority Task", "Can wait",
         (datetime.now() + timedelta(days=15)).isoformat(), 1, "pending")
    ]
    
    tasks = []
    for task_data in tasks_data:
        cursor.execute("""
            INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, task_data)
        test_db.commit()
        
        task_id = cursor.lastrowid
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        tasks.append(dict(cursor.fetchone()))
    
    # Add priority scores
    priority_data = [
        (tasks[0]['id'], 92, "v1.0-rulebased"),
        (tasks[1]['id'], 63, "v1.0-rulebased"),
        (tasks[2]['id'], 28, "v1.0-rulebased")
    ]
    
    for score_data in priority_data:
        cursor.execute("""
            INSERT INTO task_priority_scores (task_id, score, algorithm_version)
            VALUES (?, ?, ?)
        """, score_data)
    
    # Add t-shirt scores
    tshirt_data = [
        (tasks[0]['id'], "S", "Small task, quick completion", "v1.0"),
        (tasks[1]['id'], "M", "Medium complexity", "v1.0"),
        (tasks[2]['id'], "XS", "Very small task", "v1.0")
    ]
    
    for tshirt_score in tshirt_data:
        cursor.execute("""
            INSERT INTO task_tshirt_scores (task_id, tshirt_size, rationale, algorithm_version)
            VALUES (?, ?, ?, ?)
        """, tshirt_score)
    
    test_db.commit()
    
    return tasks


@pytest.fixture
def overdue_tasks(test_db, sample_user):
    """
    Create tasks with past deadlines for testing.
    """
    cursor = test_db.cursor()
    
    tasks_data = [
        (sample_user['id'], "Overdue Task 1", "Past deadline",
         (datetime.now() - timedelta(days=5)).isoformat(), 3, "pending"),
        (sample_user['id'], "Overdue Task 2", "Very overdue",
         (datetime.now() - timedelta(days=15)).isoformat(), 2, "in_progress")
    ]
    
    tasks = []
    for task_data in tasks_data:
        cursor.execute("""
            INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, task_data)
        test_db.commit()
        
        task_id = cursor.lastrowid
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        tasks.append(dict(cursor.fetchone()))
    
    return tasks


@pytest.fixture
def mixed_status_tasks(test_db, sample_user):
    """
    Create tasks with all possible status values for testing.
    """
    cursor = test_db.cursor()
    
    statuses = ['pending', 'in_progress', 'completed', 'blocked']
    tasks = []
    
    for i, status in enumerate(statuses):
        cursor.execute("""
            INSERT INTO tasks (user_id, title, description, status)
            VALUES (?, ?, ?, ?)
        """, (sample_user['id'], f"Task {status.title()}", f"Task with {status} status", status))
        test_db.commit()
        
        task_id = cursor.lastrowid
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        tasks.append(dict(cursor.fetchone()))
    
    return tasks


@pytest.fixture
def large_task_dataset(test_db, sample_user):
    """
    Create a large dataset of tasks for performance testing.
    """
    cursor = test_db.cursor()
    
    tasks = []
    for i in range(50):
        deadline = datetime.now() + timedelta(days=(i % 30))
        status = ['pending', 'in_progress', 'completed', 'blocked'][i % 4]
        
        cursor.execute("""
            INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (sample_user['id'], f"Task {i+1}", f"Description for task {i+1}",
              deadline.isoformat(), (i % 10) + 1, status))
        test_db.commit()
        
        task_id = cursor.lastrowid
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        tasks.append(dict(cursor.fetchone()))
    
    return tasks

