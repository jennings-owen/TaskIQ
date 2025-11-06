from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter(tags=["priority-scores"])


@router.get("/task_priority_scores", response_model=List[schemas.TaskPriorityScore])
def list_scores(db: Session = Depends(get_db)):
    return crud.get_priority_scores(db)


@router.post("/task_priority_scores", response_model=schemas.TaskPriorityScore)
def create_score(score: schemas.TaskPriorityScoreCreate, db: Session = Depends(get_db)):
    return crud.create_priority_score(db, score)


@router.get("/task_priority_scores/{score_id}", response_model=schemas.TaskPriorityScore)
def get_score(score_id: int, db: Session = Depends(get_db)):
    s = crud.get_priority_score(db, score_id)
    if not s:
        raise HTTPException(status_code=404, detail="Score not found")
    return s


@router.put("/task_priority_scores/{score_id}", response_model=schemas.TaskPriorityScore)
def update_score(score_id: int, score: schemas.TaskPriorityScoreCreate, db: Session = Depends(get_db)):
    s = crud.update_priority_score(db, score_id, score)
    if not s:
        raise HTTPException(status_code=404, detail="Score not found")
    return s


@router.delete("/task_priority_scores/{score_id}")
def delete_score(score_id: int, db: Session = Depends(get_db)):
    if not crud.delete_priority_score(db, score_id):
        raise HTTPException(status_code=404, detail="Score not found")
    return {"ok": True}
