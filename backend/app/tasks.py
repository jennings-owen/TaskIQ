from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
import schemas, crud
from database import get_db
from auth import get_current_active_user
import models

router = APIRouter()


@router.get("/tasks", response_model=List[schemas.Task])
def get_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Filter tasks by current user
    db_tasks = crud.get_tasks_by_user(db, current_user.id)
    results = []
    for t in db_tasks:
        # extract related priority score if present
        score = None
        if getattr(t, "priority_score", None):
            try:
                score = int(getattr(t.priority_score, "score", None))
            except Exception:
                score = None

        # extract tshirt size if present
        tshirt = None
        if getattr(t, "tshirt_score", None):
            try:
                tshirt = getattr(t.tshirt_score, "tshirt_size", None)
            except Exception:
                tshirt = None

        results.append({
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "deadline": t.deadline,
            "estimated_duration": t.estimated_duration or 0,
            "status": t.status,
            "priority_score": score or 0,
            "tshirt_size": tshirt,
        })

    return results


@router.get("/tasks/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    t = crud.get_task(db, task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Ensure user can only access their own tasks
    if t.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")

    score = None
    if getattr(t, "priority_score", None):
        try:
            score = int(getattr(t.priority_score, "score", None))
        except Exception:
            score = None

    tshirt = None
    if getattr(t, "tshirt_score", None):
        try:
            tshirt = getattr(t.tshirt_score, "tshirt_size", None)
        except Exception:
            tshirt = None

    return {
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "deadline": t.deadline,
        "estimated_duration": t.estimated_duration or 0,
        "status": t.status,
        "priority_score": score or 0,
        "tshirt_size": tshirt,
    }


@router.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    try:
        # Override user_id with current user's id
        task.user_id = current_user.id
        db_task = crud.create_task(db, task)
        
        # Format the response similar to get_task to handle related objects
        score = None
        if getattr(db_task, "priority_score", None):
            try:
                score = int(getattr(db_task.priority_score, "score", None))
            except Exception:
                score = None

        tshirt = None
        if getattr(db_task, "tshirt_score", None):
            try:
                tshirt = getattr(db_task.tshirt_score, "tshirt_size", None)
            except Exception:
                tshirt = None

        return {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "deadline": db_task.deadline,
            "estimated_duration": db_task.estimated_duration or 0,
            "status": db_task.status,
            "priority_score": score or 0,
            "tshirt_size": tshirt,
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@router.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Check if task exists and belongs to current user
    existing_task = crud.get_task(db, task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if existing_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    updated = crud.update_task(db, task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Format the response similar to get_task to handle related objects
    score = None
    if getattr(updated, "priority_score", None):
        try:
            score = int(getattr(updated.priority_score, "score", None))
        except Exception:
            score = None

    tshirt = None
    if getattr(updated, "tshirt_score", None):
        try:
            tshirt = getattr(updated.tshirt_score, "tshirt_size", None)
        except Exception:
            tshirt = None

    return {
        "id": updated.id,
        "title": updated.title,
        "description": updated.description,
        "deadline": updated.deadline,
        "estimated_duration": updated.estimated_duration or 0,
        "status": updated.status,
        "priority_score": score or 0,
        "tshirt_size": tshirt,
    }


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Check if task exists and belongs to current user
    existing_task = crud.get_task(db, task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if existing_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    
    if not crud.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True}
