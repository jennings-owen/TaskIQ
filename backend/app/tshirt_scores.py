from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import schemas, crud
from .database import get_db

router = APIRouter()


@router.get("/task_tshirt_scores", response_model=List[schemas.TaskTShirtScore])
def list_tshirts(db: Session = Depends(get_db)):
    return crud.get_tshirt_scores(db)


@router.post("/task_tshirt_scores", response_model=schemas.TaskTShirtScore)
def create_tshirt(score: schemas.TaskTShirtScoreCreate, db: Session = Depends(get_db)):
    return crud.create_tshirt_score(db, score)


@router.get("/task_tshirt_scores/{score_id}", response_model=schemas.TaskTShirtScore)
def get_tshirt(score_id: int, db: Session = Depends(get_db)):
    s = crud.get_tshirt_score(db, score_id)
    if not s:
        raise HTTPException(status_code=404, detail="T-shirt score not found")
    return s


@router.put("/task_tshirt_scores/{score_id}", response_model=schemas.TaskTShirtScore)
def update_tshirt(score_id: int, score: schemas.TaskTShirtScoreCreate, db: Session = Depends(get_db)):
    s = crud.update_tshirt_score(db, score_id, score)
    if not s:
        raise HTTPException(status_code=404, detail="T-shirt score not found")
    return s


@router.delete("/task_tshirt_scores/{score_id}")
def delete_tshirt(score_id: int, db: Session = Depends(get_db)):
    if not crud.delete_tshirt_score(db, score_id):
        raise HTTPException(status_code=404, detail="T-shirt score not found")
    return {"ok": True}
