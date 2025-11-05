from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import schemas, models
from .database import get_db
from datetime import datetime

router = APIRouter()


def _compute_score(deadline: datetime | None, estimated_duration: int | None) -> int:
    days_until_deadline = 0
    if deadline:
        days_until_deadline = (deadline.date() - datetime.now().date()).days
    score = 100 - days_until_deadline * 5 - (estimated_duration or 0) * 3
    return max(1, min(100, score))


@router.post("/ai/rank", response_model=list[schemas.AIRankResponseItem])
def ai_rank(request: schemas.AIRankRequest, db: Session = Depends(get_db), persist: bool = Query(False)):
    results = []
    for idx, task in enumerate(request.tasks, start=1):
        score = _compute_score(task.deadline, task.estimated_duration)

        # If persist requested, task_id must be provided and valid
        if persist:
            if not task.task_id:
                raise HTTPException(status_code=400, detail=f"task_id required for persistence (item index {idx})")
            db_task = db.query(models.Task).filter(models.Task.id == task.task_id).first()
            if not db_task:
                raise HTTPException(status_code=400, detail=f"task_id {task.task_id} does not exist")

            existing = db.query(models.TaskPriorityScore).filter(models.TaskPriorityScore.task_id == task.task_id).first()
            if existing:
                existing.score = score
            else:
                existing = models.TaskPriorityScore(task_id=task.task_id, score=score)
                db.add(existing)
            db.commit()

        results.append(schemas.AIRankResponseItem(task_id=task.task_id or idx, priority_score=score))

    return results


@router.post("/ai/size", response_model=schemas.AISizeResponse)
def ai_size(request: schemas.AISizeRequest, db: Session = Depends(get_db), persist: bool = Query(False)):
    gender = request.gender.lower()
    if gender == "male":
        if request.height_cm < 165:
            size = "S"
        elif request.height_cm < 180:
            size = "M"
        else:
            size = "L"
    else:
        if request.height_cm < 155:
            size = "XS"
        elif request.height_cm < 170:
            size = "S"
        else:
            size = "M"

    if persist:
        # persistence requires a task_id to be provided in the request body (not part of AISizeRequest)
        # for now, we will not allow persistence without an explicit task_id query param
        raise HTTPException(status_code=400, detail="Persistence for /ai/size requires a task-specific endpoint or task_id parameter")

    return schemas.AISizeResponse(recommended_size=size)


@router.post("/tasks/{task_id}/ai/size", response_model=schemas.AISizeResponse)
def task_ai_size(task_id: int, request: schemas.AISizeRequest, db: Session = Depends(get_db), persist: bool = Query(False)):
    """Compute a t-shirt size for a specific task and optionally persist it to task_tshirt_scores."""
    gender = request.gender.lower()
    if gender == "male":
        if request.height_cm < 165:
            size = "S"
        elif request.height_cm < 180:
            size = "M"
        else:
            size = "L"
    else:
        if request.height_cm < 155:
            size = "XS"
        elif request.height_cm < 170:
            size = "S"
        else:
            size = "M"

    # If persist requested, verify task exists and upsert into task_tshirt_scores
    if persist:
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if not db_task:
            raise HTTPException(status_code=400, detail=f"task_id {task_id} does not exist")

        existing = db.query(models.TaskTShirtScore).filter(models.TaskTShirtScore.task_id == task_id).first()
        rationale = f"height_cm={request.height_cm}, weight_kg={request.weight_kg}, gender={request.gender}, fit={request.fit_preference}"
        if existing:
            existing.tshirt_size = size
            existing.rationale = rationale
        else:
            existing = models.TaskTShirtScore(task_id=task_id, tshirt_size=size, rationale=rationale)
            db.add(existing)
        db.commit()

    return schemas.AISizeResponse(recommended_size=size)
