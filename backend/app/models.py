from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(String, default=datetime.utcnow)
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    deadline = Column(String)
    estimated_duration = Column(Integer)
    status = Column(String, default="pending")
    created_at = Column(String, default=datetime.utcnow)
    updated_at = Column(String, default=datetime.utcnow)
    user = relationship("User", back_populates="tasks")
    # relationships to TaskDependency are ambiguous because that table
    # has two foreign keys to tasks (task_id and depends_on_task_id).
    # Specify foreign_keys explicitly to disambiguate.
    dependencies = relationship(
        "TaskDependency",
        foreign_keys='[TaskDependency.task_id]',
        back_populates="task",
        cascade="all, delete-orphan",
    )
    # tasks that depend on this task
    dependents = relationship(
        "TaskDependency",
        foreign_keys='[TaskDependency.depends_on_task_id]',
        back_populates="depends_on_task",
        cascade="all, delete-orphan",
    )
    priority_score = relationship("TaskPriorityScore", uselist=False, back_populates="task", cascade="all, delete-orphan")
    tshirt_score = relationship("TaskTShirtScore", uselist=False, back_populates="task", cascade="all, delete-orphan")

class TaskDependency(Base):
    __tablename__ = "task_dependencies"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    depends_on_task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    # the task that has a dependency
    task = relationship("Task", foreign_keys=[task_id], back_populates="dependencies")
    # the task that is depended on
    depends_on_task = relationship("Task", foreign_keys=[depends_on_task_id], back_populates="dependents")

class TaskPriorityScore(Base):
    __tablename__ = "task_priority_scores"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), unique=True, nullable=False)
    score = Column(Integer, nullable=False)
    task = relationship("Task", back_populates="priority_score")

class TaskTShirtScore(Base):
    __tablename__ = "task_tshirt_scores"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), unique=True, nullable=False)
    tshirt_size = Column(String, nullable=False)
    rationale = Column(Text)
    task = relationship("Task", back_populates="tshirt_score")
