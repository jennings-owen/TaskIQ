#!/usr/bin/env python3
"""
Database seeding utility for team_synapse database.

This script executes the seed_for_user.sql file to populate the database
with tasks related to building a full stack web application for querying
books from a library's online public API.
"""

import sqlite3
import sys
import re
from pathlib import Path
from typing import Optional
import argparse


def get_database_path() -> Path:
    """
    Get the path to the team_synapse database.
    
    Returns:
        Path: Absolute path to the database.db file.
    """
    # Use the same path as defined in app/database.py
    here = Path(__file__).resolve().parent
    db_path = here / "database.db"
    return db_path


def execute_seed_for_user(
    user_id: int,
    db_path: Optional[Path] = None,
    seed_file: Optional[Path] = None
) -> None:
    """
    Execute the seed_for_user.sql file with the specified user_id.
    
    Args:
        user_id: The ID of the user to create tasks for.
        db_path: Path to database file. If None, uses default database.db.
        seed_file: Path to seed_for_user.sql file. If None, uses default location.
    
    Raises:
        FileNotFoundError: If database or seed file cannot be found.
        sqlite3.Error: If database operations fail.
        ValueError: If user_id is invalid.
    """
    if user_id <= 0:
        raise ValueError("user_id must be a positive integer")
    
    # Determine file paths
    if db_path is None:
        db_path = get_database_path()
    
    if seed_file is None:
        seed_file = Path(__file__).parent / "seed_for_user.sql"
    
    # Validate files exist
    if not db_path.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")
    
    if not seed_file.exists():
        raise FileNotFoundError(f"Seed file not found: {seed_file}")
    
    print(f"Connecting to database: {db_path}")
    print(f"Using seed file: {seed_file}")
    print(f"Creating tasks for user_id: {user_id}")
    
    # Read and process the SQL file
    with open(seed_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Replace :user_id parameter with actual value
    sql_content = sql_content.replace(':user_id', str(user_id))
    
    # Connect to database and execute
    conn = sqlite3.connect(db_path)
    
    try:
        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Execute the SQL script
        print("Executing seed script...")
        conn.executescript(sql_content)
        
        # Get count of tasks created
        cursor = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE user_id = ?", 
            (user_id,)
        )
        task_count = cursor.fetchone()[0]
        
        # Get count of dependencies created
        cursor = conn.execute("""
            SELECT COUNT(*) FROM task_dependencies td
            JOIN tasks t ON td.task_id = t.id
            WHERE t.user_id = ?
        """, (user_id,))
        dependency_count = cursor.fetchone()[0]
        
        # Get count of priority scores created
        cursor = conn.execute("""
            SELECT COUNT(*) FROM task_priority_scores tps
            JOIN tasks t ON tps.task_id = t.id
            WHERE t.user_id = ?
        """, (user_id,))
        priority_count = cursor.fetchone()[0]
        
        # Get count of t-shirt scores created
        cursor = conn.execute("""
            SELECT COUNT(*) FROM task_tshirt_scores tts
            JOIN tasks t ON tts.task_id = t.id
            WHERE t.user_id = ?
        """, (user_id,))
        tshirt_count = cursor.fetchone()[0]
        
        conn.commit()
        
        print("\n" + "="*60)
        print("SEEDING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"Tasks created: {task_count}")
        print(f"Dependencies created: {dependency_count}")
        print(f"Priority scores created: {priority_count}")
        print(f"T-shirt scores created: {tshirt_count}")
        print("="*60)
        
    except sqlite3.Error as e:
        conn.rollback()
        raise sqlite3.Error(f"Failed to execute seed script: {e}")
    
    finally:
        conn.close()


def verify_user_exists(user_id: int, db_path: Optional[Path] = None) -> bool:
    """
    Verify that a user with the given ID exists in the database.
    
    Args:
        user_id: The user ID to check.
        db_path: Path to database file. If None, uses default.
    
    Returns:
        bool: True if user exists, False otherwise.
    """
    if db_path is None:
        db_path = get_database_path()
    
    if not db_path.exists():
        return False
    
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.execute("SELECT COUNT(*) FROM users WHERE id = ?", (user_id,))
        count = cursor.fetchone()[0]
        return count > 0
    except sqlite3.Error:
        return False
    finally:
        conn.close()


def list_users(db_path: Optional[Path] = None) -> list:
    """
    List all users in the database.
    
    Args:
        db_path: Path to database file. If None, uses default.
    
    Returns:
        list: List of user dictionaries with id, name, and email.
    """
    if db_path is None:
        db_path = get_database_path()
    
    if not db_path.exists():
        return []
    
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.execute("SELECT id, name, email FROM users ORDER BY id")
        users = []
        for row in cursor.fetchall():
            users.append({
                'id': row[0],
                'name': row[1],
                'email': row[2]
            })
        return users
    except sqlite3.Error:
        return []
    finally:
        conn.close()


def clean_user_tasks(user_id: int, db_path: Optional[Path] = None) -> None:
    """
    Remove all tasks and related data for a specific user.
    
    Args:
        user_id: The user ID to clean tasks for.
        db_path: Path to database file. If None, uses default.
    
    Raises:
        sqlite3.Error: If database operations fail.
    """
    if db_path is None:
        db_path = get_database_path()
    
    if not db_path.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")
    
    conn = sqlite3.connect(db_path)
    
    try:
        # Enable foreign key constraints to ensure cascading deletes
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Get count before deletion
        cursor = conn.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?", (user_id,))
        task_count = cursor.fetchone()[0]
        
        # Delete tasks (this will cascade to related tables due to foreign keys)
        conn.execute("DELETE FROM tasks WHERE user_id = ?", (user_id,))
        
        conn.commit()
        
        print(f"Removed {task_count} tasks and related data for user_id: {user_id}")
        
    except sqlite3.Error as e:
        conn.rollback()
        raise sqlite3.Error(f"Failed to clean user tasks: {e}")
    
    finally:
        conn.close()


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Seed the team_synapse database with library book query application tasks"
    )
    
    parser.add_argument(
        "user_id",
        type=int,
        help="User ID to create tasks for"
    )
    
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing tasks for the user before seeding"
    )
    
    parser.add_argument(
        "--list-users",
        action="store_true",
        help="List all users in the database"
    )
    
    parser.add_argument(
        "--db-path",
        type=Path,
        help="Path to database file (optional)"
    )
    
    args = parser.parse_args()
    
    try:
        # List users if requested
        if args.list_users:
            users = list_users(args.db_path)
            if users:
                print("\nAvailable users:")
                print("-" * 50)
                for user in users:
                    print(f"ID: {user['id']:<3} Name: {user['name']:<20} Email: {user['email']}")
                print("-" * 50)
            else:
                print("No users found in database.")
            
            if not args.user_id:
                return
        
        # Verify user exists
        if not verify_user_exists(args.user_id, args.db_path):
            print(f"Error: User with ID {args.user_id} does not exist in the database.")
            print("Use --list-users to see available users.")
            sys.exit(1)
        
        # Clean existing tasks if requested
        if args.clean:
            print(f"Cleaning existing tasks for user_id: {args.user_id}")
            clean_user_tasks(args.user_id, args.db_path)
        
        # Execute the seed script
        execute_seed_for_user(args.user_id, args.db_path)
        
    except (FileNotFoundError, ValueError, sqlite3.Error) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()