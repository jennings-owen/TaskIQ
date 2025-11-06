from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from datetime import timedelta
from sqlalchemy.orm import Session
import schemas, crud
from database import get_db
from auth import (
    authenticate_user, 
    create_access_token, 
    create_user, 
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()

@router.post("/auth/register", response_model=schemas.Token)
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    """Register a new user."""
    db_user = create_user(db, user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login with email and password."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/login-json", response_model=schemas.Token)
def login_json(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    """Login with JSON payload (for frontend)."""
    user = authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/auth/me", response_model=schemas.User)
def get_current_user_info(current_user: schemas.User = Depends(get_current_active_user)):
    """Get current user information."""
    return current_user

@router.get("/users", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    return crud.get_users(db)


@router.post("/users", response_model=schemas.User)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@router.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    u = crud.get_user(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u


@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    u = crud.update_user(db, user_id, user)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    if not crud.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"ok": True}


@router.put("/auth/change-password")
def change_password(password_change: schemas.PasswordChange, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    """Change user password with current password verification."""
    from auth import verify_password, get_password_hash
    
    # Get the current user from database to get the stored password hash
    db_user = crud.get_user(db, current_user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if not verify_password(password_change.current_password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Hash new password
    new_password_hash = get_password_hash(password_change.new_password)
    
    # Update password in database
    db_user.password_hash = new_password_hash
    db.add(db_user)
    db.commit()
    
    return {"message": "Password changed successfully"}


@router.put("/auth/profile", response_model=schemas.User)
def update_profile(profile_update: schemas.UserProfileUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    """Update user profile (name and email only)."""
    from auth import get_user_by_email
    
    # Get the current user from database
    db_user = crud.get_user(db, current_user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if email is already taken by another user
    if profile_update.email != db_user.email:
        existing_user = get_user_by_email(db, profile_update.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Update profile
    db_user.name = profile_update.name
    db_user.email = profile_update.email
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
