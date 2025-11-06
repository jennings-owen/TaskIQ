"""Pytest configuration and fixtures for backend tests using SQLAlchemy."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("SECRET_KEY", "test-secret-key")

from app.main import app
from app.database import Base, get_db
from app.auth import get_current_active_user
from app import models

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds")


def _task_to_dict(task: models.Task) -> Dict:
    return {
        "id": task.id,
        "user_id": task.user_id,
        "title": task.title,
        "description": task.description,
        "deadline": task.deadline,
        "estimated_duration": task.estimated_duration,
        "status": task.status,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
    }


def _priority_to_dict(priority: models.TaskPriorityScore) -> Dict:
    return {
        "id": priority.id,
        "task_id": priority.task_id,
        "score": priority.score,
    }


def _tshirt_to_dict(tshirt: models.TaskTShirtScore) -> Dict:
    return {
        "id": tshirt.id,
        "task_id": tshirt.task_id,
        "tshirt_size": tshirt.tshirt_size,
        "rationale": tshirt.rationale,
    }


@pytest.fixture(scope="function")
def db_session() -> Session:
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def default_user(db_session: Session) -> models.User:
    user = models.User(
        name="Default User",
        email="default@example.com",
        password_hash="hashed",
        is_active=True,
        created_at=_now_iso(),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def client(db_session: Session, default_user: models.User):
    def override_get_db():
        yield db_session

    def override_current_user():
        return default_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_active_user] = override_current_user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_user(default_user: models.User) -> Dict:
    """Return the default user as sample user to avoid auth conflicts."""
    return {
        "id": default_user.id,
        "name": default_user.name,
        "email": default_user.email,
        "password_hash": default_user.password_hash,
    }


def _create_task(
    db: Session,
    user_id: int,
    title: str,
    description: str | None,
    deadline: str | None,
    estimated_duration: int | None,
    status: str = "pending",
) -> models.Task:
    now = _now_iso()
    task = models.Task(
        user_id=user_id,
        title=title,
        description=description,
        deadline=deadline,
        estimated_duration=estimated_duration,
        status=status,
        created_at=now,
        updated_at=now,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@pytest.fixture
def sample_tasks(db_session: Session, sample_user: Dict) -> List[Dict]:
    tasks = [
        _create_task(
            db_session,
            sample_user["id"],
            "Submit project report",
            "Send final report to manager",
            (datetime.utcnow() + timedelta(days=2)).isoformat(),
            4,
            "pending",
        ),
        _create_task(
            db_session,
            sample_user["id"],
            "Clean workspace",
            "Organize desk and files",
            (datetime.utcnow() + timedelta(days=10)).isoformat(),
            1,
            "pending",
        ),
        _create_task(
            db_session,
            sample_user["id"],
            "Review code",
            "Review pull requests",
            (datetime.utcnow() + timedelta(days=1)).isoformat(),
            2,
            "in_progress",
        ),
    ]
    return [_task_to_dict(task) for task in tasks]


@pytest.fixture
def task_data() -> Dict:
    return {
        "title": "New Task",
        "description": "Task description",
        "deadline": (datetime.utcnow() + timedelta(days=5)).isoformat(),
        "estimated_duration": 3,
        "status": "pending",
    }


@pytest.fixture
def ai_rank_data() -> Dict:
    return {
        "tasks": [
            {
                "title": "Submit project report",
                "deadline": (datetime.utcnow() + timedelta(days=2)).isoformat(),
                "estimated_duration": 4,
            },
            {
                "title": "Clean workspace",
                "deadline": (datetime.utcnow() + timedelta(days=10)).isoformat(),
                "estimated_duration": 1,
            },
        ]
    }


@pytest.fixture
def ai_size_data() -> Dict:
    return {
        "height_cm": 175,
        "weight_kg": 70,
        "gender": "male",
        "fit_preference": "regular",
    }


@pytest.fixture
def multiple_users(db_session: Session) -> List[Dict]:
    users = []
    for name, email in [
        ("Alice Smith", "alice@example.com"),
        ("Bob Jones", "bob@example.com"),
        ("Charlie Brown", "charlie@example.com"),
    ]:
        user = models.User(
            name=name,
            email=email,
            password_hash="hash",
            is_active=True,
            created_at=_now_iso(),
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        users.append({"id": user.id, "name": user.name, "email": user.email})
    return users


@pytest.fixture
def tasks_with_dependencies(db_session: Session, sample_user: Dict) -> List[Dict]:
    tasks = [
        _create_task(db_session, sample_user["id"], "Design Database", "Create schema", None, 8, "completed"),
        _create_task(db_session, sample_user["id"], "Implement API", "Build endpoints", None, 16, "in_progress"),
        _create_task(db_session, sample_user["id"], "Write Tests", "Unit and integration tests", None, 12, "pending"),
        _create_task(db_session, sample_user["id"], "Deploy Application", "Production deployment", None, 4, "blocked"),
    ]

    dependencies = [
        models.TaskDependency(task_id=tasks[1].id, depends_on_task_id=tasks[0].id),
        models.TaskDependency(task_id=tasks[2].id, depends_on_task_id=tasks[1].id),
        models.TaskDependency(task_id=tasks[3].id, depends_on_task_id=tasks[2].id),
    ]
    db_session.add_all(dependencies)
    db_session.commit()

    return [_task_to_dict(task) for task in tasks]


@pytest.fixture
def tasks_with_scores(db_session: Session, sample_user: Dict) -> List[Dict]:
    tasks = [
        _create_task(
            db_session,
            sample_user["id"],
            "High Priority Task",
            "Urgent work",
            (datetime.utcnow() + timedelta(days=1)).isoformat(),
            2,
            "pending",
        ),
        _create_task(
            db_session,
            sample_user["id"],
            "Medium Priority Task",
            "Normal work",
            (datetime.utcnow() + timedelta(days=5)).isoformat(),
            4,
            "pending",
        ),
        _create_task(
            db_session,
            sample_user["id"],
            "Low Priority Task",
            "Can wait",
            (datetime.utcnow() + timedelta(days=15)).isoformat(),
            1,
            "pending",
        ),
    ]

    priority_scores = [
        models.TaskPriorityScore(task_id=tasks[0].id, score=92),
        models.TaskPriorityScore(task_id=tasks[1].id, score=63),
        models.TaskPriorityScore(task_id=tasks[2].id, score=28),
    ]

    tshirt_scores = [
        models.TaskTShirtScore(task_id=tasks[0].id, tshirt_size="S", rationale="Small task, quick completion"),
        models.TaskTShirtScore(task_id=tasks[1].id, tshirt_size="M", rationale="Medium complexity"),
        models.TaskTShirtScore(task_id=tasks[2].id, tshirt_size="XS", rationale="Very small task"),
    ]

    db_session.add_all(priority_scores + tshirt_scores)
    db_session.commit()

    return [_task_to_dict(task) for task in tasks]


@pytest.fixture
def overdue_tasks(db_session: Session, sample_user: Dict) -> List[Dict]:
    tasks = [
        _create_task(
            db_session,
            sample_user["id"],
            "Overdue Task 1",
            "Past deadline",
            (datetime.utcnow() - timedelta(days=5)).isoformat(),
            3,
            "pending",
        ),
        _create_task(
            db_session,
            sample_user["id"],
            "Overdue Task 2",
            "Very overdue",
            (datetime.utcnow() - timedelta(days=15)).isoformat(),
            2,
            "in_progress",
        ),
    ]
    return [_task_to_dict(task) for task in tasks]


@pytest.fixture
def mixed_status_tasks(db_session: Session, sample_user: Dict) -> List[Dict]:
    tasks = []
    for status in ["pending", "in_progress", "completed", "blocked"]:
        tasks.append(
            _task_to_dict(
                _create_task(
                    db_session,
                    sample_user["id"],
                    f"Task {status.title()}",
                    f"Task with {status} status",
                    None,
                    None,
                    status,
                )
            )
        )
    return tasks


@pytest.fixture
def large_task_dataset(db_session: Session, sample_user: Dict) -> List[Dict]:
    tasks = []
    for i in range(50):
        task = _create_task(
            db_session,
            sample_user["id"],
            f"Task {i + 1}",
            f"Description for task {i + 1}",
            (datetime.utcnow() + timedelta(days=(i % 30))).isoformat(),
            (i % 10) + 1,
            ["pending", "in_progress", "completed", "blocked"][i % 4],
        )
        tasks.append(_task_to_dict(task))
    return tasks


@pytest.fixture(scope="function")
def test_db():
    """Provide a raw SQLite connection for database constraint tests."""
    import sqlite3
    from pathlib import Path
    
    # Create in-memory database with same schema
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    
    # Read and execute schema
    schema_path = Path(__file__).parent.parent / "schema.sql"
    if schema_path.exists():
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
            conn.executescript(schema_sql)
    else:
        # Fallback: create tables using SQLAlchemy models
        Base.metadata.create_all(bind=create_engine("sqlite://", creator=lambda: conn))
    
    yield conn
    conn.close()

