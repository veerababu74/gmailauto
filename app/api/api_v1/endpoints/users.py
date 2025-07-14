from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud import user
from app.schemas.user import User, UserUpdate, UserProfile
from app.api.deps import (
    get_current_user,
    get_current_active_superuser,
)

router = APIRouter()


@router.get("/me", response_model=UserProfile)
def read_user_me(current_user: User = Depends(get_current_user)) -> Any:
    """
    Get current user profile
    """
    return current_user


@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update current user (requires verified email)
    """
    updated_user = user.update(db, db_obj=current_user, obj_in=user_in)
    return updated_user


@router.get("/{user_id}", response_model=User)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by id
    """
    user_obj = user.get(db, id=user_id)
    if user_obj == current_user:
        return user_obj
    if not user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges",
        )
    return user_obj


@router.get("/", response_model=List[User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Retrieve all users (superuser only)
    """
    users = user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/gmail/connect")
def connect_gmail(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Initiate Gmail OAuth connection (requires verified email)
    """
    # This would initiate the Gmail OAuth flow
    # For now, return a placeholder
    return {
        "message": "Gmail OAuth flow would be initiated here",
        "auth_url": "https://accounts.google.com/oauth2/auth?...",
    }


@router.post("/gmail/disconnect")
def disconnect_gmail(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Disconnect Gmail account (requires verified email)
    """
    user.disconnect_gmail(db, user=current_user)
    return {"message": "Gmail account disconnected successfully"}
