from sqlalchemy.orm import Session
from typing import List, Optional
import schemas, models


def get_tasks(db: Session) -> List[models.Task]:
    return db.query(models.Task).all()


def get_tasks_by_user(db: Session, user_id: int) -> List[models.Task]:
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()


def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    data = task.dict()
    
    # Extract the optional fields that go to separate tables
    tshirt_size = data.pop("tshirt_size", None)
    priority_score = data.pop("priority_score", None)
    
    # If no user_id provided, ensure a default system user exists and use it.
    if not data.get("user_id"):
        system = db.query(models.User).filter(models.User.email == "system@local").first()
        if not system:
            system = models.User(name="system", email="system@local", password_hash="")
            db.add(system)
            db.commit()
            db.refresh(system)
        data["user_id"] = system.id
    else:
        # If a user_id was supplied, validate it exists to avoid DB integrity errors.
        supplied = data.get("user_id")
        user = db.query(models.User).filter(models.User.id == supplied).first()
        if not user:
            # Raise a ValueError so the HTTP layer can return a 400 with a helpful message
            raise ValueError(f"user_id {supplied} does not exist")

    # Create the main task
    db_task = models.Task(**data)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Create related t-shirt size record if provided
    if tshirt_size:
        tshirt_record = models.TaskTShirtScore(
            task_id=db_task.id,
            tshirt_size=tshirt_size,
            rationale="User specified"
        )
        db.add(tshirt_record)
    
    # Create related priority score record if provided
    if priority_score:
        priority_record = models.TaskPriorityScore(
            task_id=db_task.id,
            score=priority_score
        )
        db.add(priority_record)
    
    # Commit the related records
    if tshirt_size or priority_score:
        db.commit()
        db.refresh(db_task)
    
    return db_task


def update_task(db: Session, task_id: int, task: schemas.TaskUpdate) -> Optional[models.Task]:
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    
    # Get the task data as dict and extract special fields
    task_data = task.dict(exclude_unset=True)
    priority_score = task_data.pop('priority_score', None)
    tshirt_size = task_data.pop('tshirt_size', None)
    
    # Update main task fields
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    # Update priority score if provided
    if priority_score is not None:
        if db_task.priority_score:
            # Update existing priority score
            db_task.priority_score.score = priority_score
        else:
            # Create new priority score
            priority_score_obj = models.TaskPriorityScore(
                task_id=task_id,
                score=priority_score
            )
            db.add(priority_score_obj)
    
    # Update t-shirt size if provided
    if tshirt_size is not None:
        if db_task.tshirt_score:
            # Update existing t-shirt score
            db_task.tshirt_score.tshirt_size = tshirt_size
        else:
            # Create new t-shirt score
            tshirt_score_obj = models.TaskTShirtScore(
                task_id=task_id,
                tshirt_size=tshirt_size
            )
            db.add(tshirt_score_obj)
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True


## Users CRUD
def get_users(db: Session) -> List[models.User]:
    return db.query(models.User).all()


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    data = user.dict()
    db_user = models.User(**data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserCreate) -> Optional[models.User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True


## Task dependency CRUD
def get_task_dependencies(db: Session) -> List[models.TaskDependency]:
    return db.query(models.TaskDependency).all()


def create_task_dependency(db: Session, dep: schemas.TaskDependencyCreate) -> models.TaskDependency:
    data = dep.dict()
    db_dep = models.TaskDependency(**data)
    db.add(db_dep)
    db.commit()
    db.refresh(db_dep)
    return db_dep


def delete_task_dependency(db: Session, dep_id: int) -> bool:
    db_dep = db.query(models.TaskDependency).filter(models.TaskDependency.id == dep_id).first()
    if not db_dep:
        return False
    db.delete(db_dep)
    db.commit()
    return True


## Task priority score CRUD
def get_priority_scores(db: Session) -> List[models.TaskPriorityScore]:
    return db.query(models.TaskPriorityScore).all()


def get_priority_score(db: Session, score_id: int) -> Optional[models.TaskPriorityScore]:
    return db.query(models.TaskPriorityScore).filter(models.TaskPriorityScore.id == score_id).first()


def create_priority_score(db: Session, score: schemas.TaskPriorityScoreCreate) -> models.TaskPriorityScore:
    data = score.dict()
    db_score = models.TaskPriorityScore(**data)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score


def update_priority_score(db: Session, score_id: int, score: schemas.TaskPriorityScoreCreate) -> Optional[models.TaskPriorityScore]:
    db_score = get_priority_score(db, score_id)
    if not db_score:
        return None
    for key, value in score.dict(exclude_unset=True).items():
        setattr(db_score, key, value)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score


def delete_priority_score(db: Session, score_id: int) -> bool:
    db_score = get_priority_score(db, score_id)
    if not db_score:
        return False
    db.delete(db_score)
    db.commit()
    return True


## T-shirt score CRUD
def get_tshirt_scores(db: Session) -> List[models.TaskTShirtScore]:
    return db.query(models.TaskTShirtScore).all()


def get_tshirt_score(db: Session, score_id: int) -> Optional[models.TaskTShirtScore]:
    return db.query(models.TaskTShirtScore).filter(models.TaskTShirtScore.id == score_id).first()


def create_tshirt_score(db: Session, score: schemas.TaskTShirtScoreCreate) -> models.TaskTShirtScore:
    data = score.dict()
    db_score = models.TaskTShirtScore(**data)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score


def update_tshirt_score(db: Session, score_id: int, score: schemas.TaskTShirtScoreCreate) -> Optional[models.TaskTShirtScore]:
    db_score = get_tshirt_score(db, score_id)
    if not db_score:
        return None
    for key, value in score.dict(exclude_unset=True).items():
        setattr(db_score, key, value)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score


def delete_tshirt_score(db: Session, score_id: int) -> bool:
    db_score = get_tshirt_score(db, score_id)
    if not db_score:
        return False
    db.delete(db_score)
    db.commit()
    return True
