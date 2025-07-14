from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import math

from app.api.deps import get_db, get_current_user
from app.crud.crud_default_sender import default_sender
from app.schemas.default_sender import (
    DefaultSenderCreate,
    DefaultSenderUpdate,
    DefaultSenderResponse,
    DefaultSenderListResponse,
    DefaultSenderBulkCreate,
    DefaultSenderBulkDelete,
)
from app.schemas.user import User

router = APIRouter()


@router.get("/", response_model=DefaultSenderListResponse)
def get_default_senders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search in email and description"),
):
    """
    Get all default senders with pagination and filtering
    """
    items, total = default_sender.get_multi(
        db, skip=skip, limit=limit, is_active=is_active, search=search
    )

    return DefaultSenderListResponse(
        items=items,
        total=total,
        page=skip // limit + 1,
        per_page=limit,
        total_pages=math.ceil(total / limit) if total > 0 else 0,
    )


@router.get("/active", response_model=List[DefaultSenderResponse])
def get_active_default_senders(db: Session = Depends(get_db)):
    """
    Get all active default senders
    """
    return default_sender.get_active(db)


@router.get("/emails", response_model=List[str])
def get_default_sender_emails(
    db: Session = Depends(get_db),
    is_active: bool = Query(True, description="Get active or inactive emails"),
):
    """
    Get list of default sender email addresses only
    """
    return default_sender.get_emails_list(db, is_active=is_active)


@router.get("/{sender_id}", response_model=DefaultSenderResponse)
def get_default_sender(sender_id: int, db: Session = Depends(get_db)):
    """
    Get a single default sender by ID
    """
    db_sender = default_sender.get(db, id=sender_id)
    if not db_sender:
        raise HTTPException(status_code=404, detail="Default sender not found")
    return db_sender


@router.post("/", response_model=DefaultSenderResponse)
def create_default_sender(
    sender_in: DefaultSenderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new default sender
    """
    # Check if email already exists
    existing_sender = default_sender.get_by_email(db, sender_in.email)
    if existing_sender:
        raise HTTPException(
            status_code=400, detail="A default sender with this email already exists"
        )

    return default_sender.create(db, obj_in=sender_in)


@router.post("/bulk", response_model=List[DefaultSenderResponse])
def bulk_create_default_senders(
    bulk_data: DefaultSenderBulkCreate, db: Session = Depends(get_db)
):
    """
    Bulk create default senders
    """
    return default_sender.bulk_create(db, objs_in=bulk_data.senders)


@router.put("/{sender_id}", response_model=DefaultSenderResponse)
def update_default_sender(
    sender_id: int, sender_update: DefaultSenderUpdate, db: Session = Depends(get_db)
):
    """
    Update a default sender
    """
    db_sender = default_sender.get(db, id=sender_id)
    if not db_sender:
        raise HTTPException(status_code=404, detail="Default sender not found")

    # Check if email is being updated and if it already exists
    if sender_update.email and sender_update.email != db_sender.email:
        existing_sender = default_sender.get_by_email(db, sender_update.email)
        if existing_sender:
            raise HTTPException(
                status_code=400,
                detail="A default sender with this email already exists",
            )

    return default_sender.update(db, db_obj=db_sender, obj_in=sender_update)


@router.delete("/{sender_id}", response_model=DefaultSenderResponse)
def delete_default_sender(
    sender_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a single default sender
    """
    db_sender = default_sender.remove(db, id=sender_id)
    if not db_sender:
        raise HTTPException(status_code=404, detail="Default sender not found")
    return db_sender


@router.delete("/bulk/delete")
def bulk_delete_default_senders(
    bulk_data: DefaultSenderBulkDelete, db: Session = Depends(get_db)
):
    """
    Bulk delete default senders
    """
    deleted_count = default_sender.bulk_delete(db, ids=bulk_data.sender_ids)
    return {
        "message": f"Deleted {deleted_count} default senders",
        "deleted_count": deleted_count,
    }


@router.delete("/")
def delete_all_default_senders(db: Session = Depends(get_db)):
    """
    Delete all default senders
    """
    all_senders = default_sender.get_multi(db, limit=10000)[0]  # Get all
    sender_ids = [sender.id for sender in all_senders]
    deleted_count = default_sender.bulk_delete(db, ids=sender_ids)
    return {
        "message": f"Deleted all {deleted_count} default senders",
        "deleted_count": deleted_count,
    }


@router.put("/activate/all")
def activate_all_default_senders(db: Session = Depends(get_db)):
    """
    Activate all default senders
    """
    updated_count = default_sender.activate_all(db)
    return {
        "message": f"Activated {updated_count} default senders",
        "updated_count": updated_count,
    }


@router.put("/deactivate/all")
def deactivate_all_default_senders(db: Session = Depends(get_db)):
    """
    Deactivate all default senders
    """
    updated_count = default_sender.deactivate_all(db)
    return {
        "message": f"Deactivated {updated_count} default senders",
        "updated_count": updated_count,
    }
