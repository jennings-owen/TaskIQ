"""
Test database setup utility.

This module provides functions to create and populate a test database
using schema.sql and seed_data.sql files during test execution.
"""

import sqlite3
from pathlib import Path
from typing import Optional


def create_test_database(
    db_path: Optional[str] = None,
    schema_file: Optional[Path] = None,
    seed_file: Optional[Path] = None
) -> sqlite3.Connection:
    """
    Create and populate a test database from SQL files.
    
    Args:
        db_path: Path to database file. If None, creates in-memory database.
        schema_file: Path to schema.sql file. If None, uses default location.
        seed_file: Path to seed_data.sql file. If None, uses default location.
    
    Returns:
        sqlite3.Connection: Connection to the populated test database.
    
    Raises:
        FileNotFoundError: If schema or seed files cannot be found.
        sqlite3.Error: If database creation or population fails.
    """
    # Determine file paths
    if schema_file is None:
        schema_file = Path(__file__).parent.parent / "schema.sql"
    
    if seed_file is None:
        seed_file = Path(__file__).parent.parent / "seed_data.sql"
    
    # Validate files exist
    if not schema_file.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_file}")
    
    if not seed_file.exists():
        raise FileNotFoundError(f"Seed data file not found: {seed_file}")
    
    # Create database connection
    if db_path is None:
        conn = sqlite3.connect(":memory:")
    else:
        conn = sqlite3.connect(db_path)
    
    # Enable foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON")
    
    try:
        # Execute schema
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
            conn.executescript(schema_sql)
        
        # Execute seed data
        with open(seed_file, 'r', encoding='utf-8') as f:
            seed_sql = f.read()
            conn.executescript(seed_sql)
        
        conn.commit()
        
    except sqlite3.Error as e:
        conn.close()
        raise sqlite3.Error(f"Failed to create test database: {e}")
    
    return conn


def create_minimal_test_database(db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Create a test database with schema only (no seed data).
    
    Args:
        db_path: Path to database file. If None, creates in-memory database.
    
    Returns:
        sqlite3.Connection: Connection to the test database.
    
    Raises:
        FileNotFoundError: If schema file cannot be found.
        sqlite3.Error: If database creation fails.
    """
    schema_file = Path(__file__).parent.parent / "schema.sql"
    
    if not schema_file.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_file}")
    
    # Create database connection
    if db_path is None:
        conn = sqlite3.connect(":memory:")
    else:
        conn = sqlite3.connect(db_path)
    
    # Enable foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON")
    
    try:
        # Execute schema
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
            conn.executescript(schema_sql)
        
        conn.commit()
        
    except sqlite3.Error as e:
        conn.close()
        raise sqlite3.Error(f"Failed to create test database: {e}")
    
    return conn


def insert_test_user(conn: sqlite3.Connection, user_data: dict) -> int:
    """
    Insert a test user into the database.
    
    Args:
        conn: Database connection.
        user_data: Dictionary with user fields (name, email, password_hash).
    
    Returns:
        int: ID of the inserted user.
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (name, email, password_hash)
        VALUES (?, ?, ?)
    """, (
        user_data.get('name', 'Test User'),
        user_data.get('email', 'test@example.com'),
        user_data.get('password_hash', 'hashed_password')
    ))
    conn.commit()
    return cursor.lastrowid


def insert_test_task(conn: sqlite3.Connection, task_data: dict) -> int:
    """
    Insert a test task into the database.
    
    Args:
        conn: Database connection.
        task_data: Dictionary with task fields.
    
    Returns:
        int: ID of the inserted task.
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (user_id, title, description, deadline, estimated_duration, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        task_data['user_id'],
        task_data.get('title', 'Test Task'),
        task_data.get('description'),
        task_data.get('deadline'),
        task_data.get('estimated_duration'),
        task_data.get('status', 'pending')
    ))
    conn.commit()
    return cursor.lastrowid


def get_user_by_email(conn: sqlite3.Connection, email: str) -> Optional[dict]:
    """
    Retrieve a user by email address.
    
    Args:
        conn: Database connection.
        email: User's email address.
    
    Returns:
        dict: User data or None if not found.
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, email, password_hash, is_active, created_at
        FROM users
        WHERE email = ?
    """, (email,))
    
    row = cursor.fetchone()
    if row:
        return {
            'id': row[0],
            'name': row[1],
            'email': row[2],
            'password_hash': row[3],
            'is_active': row[4],
            'created_at': row[5]
        }
    return None


def get_tasks_by_user(conn: sqlite3.Connection, user_id: int) -> list:
    """
    Retrieve all tasks for a user.
    
    Args:
        conn: Database connection.
        user_id: User's ID.
    
    Returns:
        list: List of task dictionaries.
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, user_id, title, description, deadline, estimated_duration, 
               status, created_at, updated_at
        FROM tasks
        WHERE user_id = ?
    """, (user_id,))
    
    tasks = []
    for row in cursor.fetchall():
        tasks.append({
            'id': row[0],
            'user_id': row[1],
            'title': row[2],
            'description': row[3],
            'deadline': row[4],
            'estimated_duration': row[5],
            'status': row[6],
            'created_at': row[7],
            'updated_at': row[8]
        })
    return tasks


if __name__ == "__main__":
    """
    Example usage: Create a test database file.
    """
    import sys
    
    if len(sys.argv) > 1:
        db_file = sys.argv[1]
    else:
        db_file = Path(__file__).parent / "test.db"
    
    print(f"Creating test database: {db_file}")
    
    try:
        conn = create_test_database(str(db_file))
        
        # Verify database contents
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tasks")
        task_count = cursor.fetchone()[0]
        
        print(f"Database created successfully!")
        print(f"  Users: {user_count}")
        print(f"  Tasks: {task_count}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error creating database: {e}", file=sys.stderr)
        sys.exit(1)

