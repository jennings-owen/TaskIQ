from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    estimated_duration: Optional[int] = None
    status: Optional[str] = "pending"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

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
