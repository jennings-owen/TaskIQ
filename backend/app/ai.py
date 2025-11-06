from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from datetime import datetime

router = APIRouter(tags=["ai"])


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
def ai_size(request: schemas.TaskSizeRequest, db: Session = Depends(get_db), persist: bool = Query(False)):
    """
    Estimate task complexity using T-shirt sizing (XS, S, M, L, XL).
    
    T-shirt sizing is an Agile estimation technique that represents relative effort,
    complexity, and scope of tasks. Factors considered:
    - Title/description complexity (keywords, length)
    - Estimated duration (hours)
    - Deadline urgency
    - Dependencies (if provided)
    """
    size, rationale = _estimate_task_size(
        title=request.title,
        description=request.description,
        estimated_duration=request.estimated_duration,
        deadline=request.deadline,
        has_dependencies=request.has_dependencies
    )

    if persist and request.task_id:
        db_task = db.query(models.Task).filter(models.Task.id == request.task_id).first()
        if not db_task:
            raise HTTPException(status_code=400, detail=f"task_id {request.task_id} does not exist")

        existing = db.query(models.TaskTShirtScore).filter(models.TaskTShirtScore.task_id == request.task_id).first()
        if existing:
            existing.tshirt_size = size
            existing.rationale = rationale
        else:
            existing = models.TaskTShirtScore(task_id=request.task_id, tshirt_size=size, rationale=rationale)
            db.add(existing)
        db.commit()

    return schemas.AISizeResponse(recommended_size=size, rationale=rationale)


def _estimate_task_size(
    title: str,
    description: str | None,
    estimated_duration: int | None,
    deadline: datetime | None,
    has_dependencies: bool = False
) -> tuple[str, str]:
    """
    Estimate task size based on complexity factors.
    
    Scoring factors (0-115 points total):
    - Estimated duration (0-40 points): Based on hours to complete
    - Title/description complexity (0-30 points): Keyword analysis
    - Description length (0-15 points): Scope indicator
    - Dependencies (0-15 points): Coordination overhead
    - Deadline urgency (0-15 points): Time pressure factor
    
    Returns: (size, rationale) tuple where size is XS/S/M/L/XL
    """
    complexity_score = 0
    factors = []
    
    # Factor 1: Estimated duration (0-40 points)
    if estimated_duration:
        if estimated_duration <= 2:
            complexity_score += 5
            factors.append(f"duration: {estimated_duration}h (quick)")
        elif estimated_duration <= 8:
            complexity_score += 15
            factors.append(f"duration: {estimated_duration}h (moderate)")
        elif estimated_duration <= 24:
            complexity_score += 30
            factors.append(f"duration: {estimated_duration}h (substantial)")
        else:
            complexity_score += 40
            factors.append(f"duration: {estimated_duration}h (extensive)")
    else:
        complexity_score += 10
        factors.append("duration: unknown (assumed moderate)")
    
    # Factor 2: Title/description complexity (0-30 points)
    title_lower = title.lower()
    desc_lower = (description or "").lower()
    combined_text = title_lower + " " + desc_lower
    
    # Check for complexity keywords
    complex_keywords = ["refactor", "redesign", "migrate", "integrate", "architecture", 
                        "security", "performance", "optimization", "database", "api"]
    simple_keywords = ["fix", "update", "add", "remove", "change", "typo", "text"]
    
    complex_count = sum(1 for kw in complex_keywords if kw in combined_text)
    simple_count = sum(1 for kw in simple_keywords if kw in combined_text)
    
    if complex_count >= 2:
        complexity_score += 30
        factors.append("complexity: high (multiple complex keywords)")
    elif complex_count >= 1:
        complexity_score += 20
        factors.append("complexity: moderate (complex keywords)")
    elif simple_count >= 1:
        complexity_score += 5
        factors.append("complexity: low (simple task)")
    else:
        complexity_score += 15
        factors.append("complexity: moderate (neutral)")
    
    # Factor 3: Description length (0-15 points)
    if description and len(description) > 200:
        complexity_score += 15
        factors.append("scope: detailed requirements")
    elif description and len(description) > 50:
        complexity_score += 8
        factors.append("scope: moderate requirements")
    else:
        complexity_score += 3
        factors.append("scope: brief requirements")
    
    # Factor 4: Dependencies (0-15 points)
    if has_dependencies:
        complexity_score += 15
        factors.append("dependencies: yes (coordination needed)")
    
    # Factor 5: Deadline urgency (0-15 points)
    if deadline:
        try:
            now = datetime.utcnow()
            # Handle both datetime objects and strings
            if isinstance(deadline, str):
                from dateutil import parser
                deadline_dt = parser.parse(deadline)
            else:
                deadline_dt = deadline
            
            # Calculate days until deadline
            delta = deadline_dt - now
            days_until = delta.total_seconds() / 86400
            
            if days_until < 0:
                # Overdue - maximum urgency
                complexity_score += 15
                factors.append(f"deadline: overdue by {abs(days_until):.1f} days (critical)")
            elif days_until <= 1:
                # Due within 1 day
                complexity_score += 15
                factors.append(f"deadline: {days_until:.1f} days (critical)")
            elif days_until <= 3:
                # Due within 3 days
                complexity_score += 12
                factors.append(f"deadline: {days_until:.1f} days (very urgent)")
            elif days_until <= 7:
                # Due within 1 week
                complexity_score += 8
                factors.append(f"deadline: {days_until:.1f} days (urgent)")
            elif days_until <= 14:
                # Due within 2 weeks
                complexity_score += 4
                factors.append(f"deadline: {days_until:.1f} days (moderate urgency)")
            else:
                # More than 2 weeks away
                complexity_score += 0
                factors.append(f"deadline: {days_until:.1f} days (comfortable)")
        except Exception as e:
            # If deadline parsing fails, don't add urgency but note it
            factors.append("deadline: could not parse")
    
    # Map complexity score to T-shirt size
    # Total possible: 0-115 points (updated to include deadline factor)
    if complexity_score <= 23:  # ~20% of 115
        size = "XS"
    elif complexity_score <= 46:  # ~40% of 115
        size = "S"
    elif complexity_score <= 69:  # ~60% of 115
        size = "M"
    elif complexity_score <= 92:  # ~80% of 115
        size = "L"
    else:
        size = "XL"
    
    rationale = f"Score: {complexity_score}/115. Factors: {'; '.join(factors)}"
    return size, rationale


@router.post("/tasks/{task_id}/ai/size", response_model=schemas.AISizeResponse)
def task_ai_size(task_id: int, db: Session = Depends(get_db), persist: bool = Query(True)):
    """
    Estimate T-shirt size for an existing task based on its attributes.
    Automatically persists the result to task_tshirt_scores.
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    # Check if task has dependencies
    has_dependencies = db.query(models.TaskDependency).filter(
        models.TaskDependency.task_id == task_id
    ).first() is not None
    
    size, rationale = _estimate_task_size(
        title=db_task.title,
        description=db_task.description,
        estimated_duration=db_task.estimated_duration,
        deadline=db_task.deadline,
        has_dependencies=has_dependencies
    )
    
    if persist:
        existing = db.query(models.TaskTShirtScore).filter(
            models.TaskTShirtScore.task_id == task_id
        ).first()
        if existing:
            existing.tshirt_size = size
            existing.rationale = rationale
        else:
            existing = models.TaskTShirtScore(task_id=task_id, tshirt_size=size, rationale=rationale)
            db.add(existing)
        db.commit()
    
    return schemas.AISizeResponse(recommended_size=size, rationale=rationale)
