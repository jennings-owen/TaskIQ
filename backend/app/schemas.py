from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    estimated_duration: Optional[int] = None
    status: Optional[str] = "pending"

    @validator("deadline", pre=True)
    def _coerce_deadline(cls, v):
        # Accept empty string as no deadline
        if v == "":
            return None
        return v

    @validator("estimated_duration", pre=True)
    def _coerce_estimated_duration(cls, v):
        # Accept empty string and numeric strings
        if v == "":
            return None
        if isinstance(v, str) and v.isdigit():
            return int(v)
        return v

class TaskCreate(TaskBase):
    # Optional user_id so frontend can omit it for simple flows. If omitted,
    # the backend will attach the task to a default user (created if needed).
    user_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    estimated_duration: Optional[int] = None
    status: Optional[str] = None

    @validator("deadline", pre=True)
    def _coerce_deadline_update(cls, v):
        if v == "":
            return None
        return v

    @validator("estimated_duration", pre=True)
    def _coerce_estimated_duration_update(cls, v):
        if v == "":
            return None
        if isinstance(v, str) and v.isdigit():
            return int(v)
        return v

class Task(TaskBase):
    id: int
    priority_score: Optional[int] = None
    tshirt_size: Optional[str] = None
    class Config:
        orm_mode = True

class AIRankRequestTask(BaseModel):
    title: str
    task_id: Optional[int] = None
    deadline: Optional[datetime] = None
    estimated_duration: Optional[int] = None

class AIRankRequest(BaseModel):
    tasks: List[AIRankRequestTask]

class AIRankResponseItem(BaseModel):
    task_id: int
    priority_score: int

class AISizeRequest(BaseModel):
    height_cm: int
    weight_kg: int
    gender: str
    fit_preference: str

class AISizeResponse(BaseModel):
    recommended_size: str


class UserCreate(BaseModel):
    name: str
    email: str
    password_hash: Optional[str] = None


class User(BaseModel):
    id: int
    name: str
    email: str
    password_hash: Optional[str] = None
    created_at: Optional[datetime] = None
    class Config:
        orm_mode = True


class TaskDependencyCreate(BaseModel):
    task_id: int
    depends_on_task_id: int


class TaskDependency(BaseModel):
    id: int
    task_id: int
    depends_on_task_id: int
    class Config:
        orm_mode = True


class TaskPriorityScoreCreate(BaseModel):
    task_id: int
    score: int


class TaskPriorityScore(BaseModel):
    id: int
    task_id: int
    score: int
    class Config:
        orm_mode = True


class TaskTShirtScoreCreate(BaseModel):
    task_id: int
    tshirt_size: str
    rationale: Optional[str] = None


class TaskTShirtScore(BaseModel):
    id: int
    task_id: int
    tshirt_size: str
    rationale: Optional[str] = None
    class Config:
        orm_mode = True
