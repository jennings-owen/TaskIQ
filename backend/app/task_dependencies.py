from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter(tags=["task-dependencies"])


@router.get("/tasks/dependencies", response_model=List[schemas.TaskDependency])
def list_deps(db: Session = Depends(get_db)):
    return crud.get_task_dependencies(db)


@router.post("/tasks/dependencies", response_model=schemas.TaskDependency)
def create_dep(dep: schemas.TaskDependencyCreate, db: Session = Depends(get_db)):
    return crud.create_task_dependency(db, dep)


@router.delete("/tasks/dependencies/{dep_id}")
def delete_dep(dep_id: int, db: Session = Depends(get_db)):
    if not crud.delete_task_dependency(db, dep_id):
        raise HTTPException(status_code=404, detail="Dependency not found")
    return {"ok": True}
