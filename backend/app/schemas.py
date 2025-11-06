from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, validator

class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    estimated_duration: Optional[int] = None
    status: Optional[str] = "pending"

    @validator("title")
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v

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
    
    @validator("estimated_duration")
    def validate_estimated_duration(cls, v):
        if v is not None and v < 0:
            raise ValueError("Estimated duration must be non-negative")
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
    
    @validator("estimated_duration")
    def validate_estimated_duration(cls, v):
        if v is not None and v < 0:
            raise ValueError("Estimated duration must be non-negative")
        return v

class TaskResponse(TaskBase):
    id: int
    user_id: int
    priority_score: Optional[int] = None
    tshirt_size: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class TaskPriorityDetail(BaseModel):
    task_id: int
    score: int


class TaskTShirtDetail(BaseModel):
    task_id: int
    tshirt_size: str
    rationale: Optional[str] = None

class AIRankRequestTask(BaseModel):
    title: str
    task_id: Optional[int] = None
    deadline: Optional[datetime] = None
    estimated_duration: Optional[int] = None

    @validator("estimated_duration")
    def validate_estimated_duration(cls, v):
        if v is not None and v < 0:
            raise ValueError("Estimated duration cannot be negative")
        return v

class AIRankRequest(BaseModel):
    tasks: List[AIRankRequestTask]

class AIRankResponseItem(BaseModel):
    task_id: int
    priority_score: int

class TaskSizeRequest(BaseModel):
    """
    Request for T-shirt size estimation of a task.
    
    T-shirt sizing is an Agile estimation technique for relative effort/complexity.
    """
    title: str
    description: Optional[str] = None
    estimated_duration: Optional[int] = None
    deadline: Optional[datetime] = None
    has_dependencies: bool = False
    task_id: Optional[int] = None  # For persistence

    @validator("title")
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v

    @validator("estimated_duration")
    def validate_estimated_duration(cls, v):
        if v is not None and v < 0:
            raise ValueError("Estimated duration cannot be negative")
        return v


# Keep old AISizeRequest for backward compatibility (deprecated)
class AISizeRequest(BaseModel):
    """DEPRECATED: Use TaskSizeRequest instead. This is for physical t-shirt sizing."""
    height_cm: int
    weight_kg: int
    gender: str
    fit_preference: str

    @validator("height_cm")
    def validate_height(cls, v):
        if v <= 0:
            raise ValueError("Height must be positive")
        return v

    @validator("weight_kg")
    def validate_weight(cls, v):
        if v <= 0:
            raise ValueError("Weight must be positive")
        return v

    @validator("gender")
    def validate_gender(cls, v):
        allowed_genders = ["male", "female", "unisex"]
        if v.lower() not in allowed_genders:
            raise ValueError(f"Gender must be one of: {', '.join(allowed_genders)}")
        return v.lower()

    @validator("fit_preference")
    def validate_fit_preference(cls, v):
        allowed_fits = ["slim", "regular", "loose"]
        if v.lower() not in allowed_fits:
            raise ValueError(f"Fit preference must be one of: {', '.join(allowed_fits)}")
        return v.lower()


class AISizeResponse(BaseModel):
    recommended_size: str
    rationale: Optional[str] = None


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
