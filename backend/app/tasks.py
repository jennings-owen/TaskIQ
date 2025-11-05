from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from . import schemas, crud
from .database import get_db

router = APIRouter()


@router.get("/tasks", response_model=List[schemas.Task])
def get_tasks(db: Session = Depends(get_db)):
    db_tasks = crud.get_tasks(db)
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


@router.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)


@router.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    updated = crud.update_task(db, task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    if not crud.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True}
