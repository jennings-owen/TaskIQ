from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    estimated_duration: Optional[int] = None
    status: Optional[str] = "pending"

    @validator("status")
    def validate_status(cls, v):
        allowed_statuses = ["pending", "in_progress", "completed", "blocked"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return v

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
    # Optional fields for t-shirt size and priority score
    tshirt_size: Optional[str] = None
    priority_score: Optional[int] = None

    @validator("tshirt_size")
    def validate_tshirt_size(cls, v):
        if v is not None:
            allowed_sizes = ["XS", "S", "M", "L", "XL"]
            if v not in allowed_sizes:
                raise ValueError(f"T-shirt size must be one of: {', '.join(allowed_sizes)}")
        return v

    @validator("priority_score")
    def validate_priority_score(cls, v):
        if v is not None and (v < 1 or v > 100):
            raise ValueError("Priority score must be between 1 and 100")
        return v

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    estimated_duration: Optional[int] = None
    status: Optional[str] = None
    priority_score: Optional[int] = None
    tshirt_size: Optional[str] = None

    @validator("status")
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = ["pending", "in_progress", "completed", "blocked"]
            if v not in allowed_statuses:
                raise ValueError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return v

    @validator("tshirt_size")
    def validate_tshirt_size(cls, v):
        if v is not None:
            allowed_sizes = ["XS", "S", "M", "L", "XL"]
            if v not in allowed_sizes:
                raise ValueError(f"T-shirt size must be one of: {', '.join(allowed_sizes)}")
        return v

    @validator("priority_score")
    def validate_priority_score(cls, v):
        if v is not None:
            if not (1 <= v <= 100):
                raise ValueError("Priority score must be between 1 and 100")
        return v

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
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    created_at: Optional[datetime] = None
    class Config:
        orm_mode = True


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


class UserProfileUpdate(BaseModel):
    name: str
    email: str


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
