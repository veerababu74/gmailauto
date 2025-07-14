from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import math
from datetime import datetime

from app.api.deps import get_db
from app.crud.crud_spam_handler_data import spam_handler_data
from app.schemas.spam_handler_data import (
    SpamHandlerDataCreate,
    SpamHandlerDataUpdate,
    SpamHandlerDataResponse,
    SpamHandlerDataListResponse,
    SpamHandlerDataBulkCreate,
    SpamHandlerDataBulkDelete,
    SpamHandlerDataStats,
)

router = APIRouter()


@router.get("/", response_model=SpamHandlerDataListResponse)
def get_spam_handler_data(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    agent_name: Optional[str] = Query(None, description="Filter by agent name"),
    profile_name: Optional[str] = Query(None, description="Filter by profile name"),
    sender_email: Optional[str] = Query(None, description="Filter by sender email"),
    error_occurred: Optional[bool] = Query(None, description="Filter by error status"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    search: Optional[str] = Query(None, description="Search in multiple fields"),
):
    """
    Get all spam handler data entries with pagination and filtering
    """
    items, total = spam_handler_data.get_multi(
        db,
        skip=skip,
        limit=limit,
        agent_name=agent_name,
        profile_name=profile_name,
        sender_email=sender_email,
        error_occurred=error_occurred,
        start_date=start_date,
        end_date=end_date,
        search=search,
    )

    return SpamHandlerDataListResponse(
        items=items,
        total=total,
        page=skip // limit + 1,
        per_page=limit,
        total_pages=math.ceil(total / limit) if total > 0 else 0,
    )


@router.get("/recent", response_model=List[SpamHandlerDataResponse])
def get_recent_spam_handler_data(
    db: Session = Depends(get_db),
    hours: int = Query(24, ge=1, le=168, description="Number of hours to look back"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of entries to return"
    ),
):
    """
    Get recent spam handler data entries within specified hours
    """
    return spam_handler_data.get_recent_entries(db, hours=hours, limit=limit)


@router.get("/statistics", response_model=SpamHandlerDataStats)
def get_spam_handler_statistics(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(
        None, description="Start date for statistics"
    ),
    end_date: Optional[datetime] = Query(None, description="End date for statistics"),
):
    """
    Get spam handler statistics
    """
    stats = spam_handler_data.get_statistics(
        db, start_date=start_date, end_date=end_date
    )
    return SpamHandlerDataStats(**stats)


@router.get("/by-agent/{agent_name}", response_model=List[SpamHandlerDataResponse])
def get_spam_handler_data_by_agent(
    agent_name: str,
    db: Session = Depends(get_db),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of entries to return"
    ),
):
    """
    Get spam handler data by agent name
    """
    return spam_handler_data.get_by_agent(db, agent_name=agent_name, limit=limit)


@router.get("/by-profile/{profile_name}", response_model=List[SpamHandlerDataResponse])
def get_spam_handler_data_by_profile(
    profile_name: str,
    db: Session = Depends(get_db),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of entries to return"
    ),
):
    """
    Get spam handler data by profile name
    """
    return spam_handler_data.get_by_profile(db, profile_name=profile_name, limit=limit)


@router.get("/by-sender/{sender_email}", response_model=List[SpamHandlerDataResponse])
def get_spam_handler_data_by_sender(
    sender_email: str,
    db: Session = Depends(get_db),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of entries to return"
    ),
):
    """
    Get spam handler data by sender email
    """
    return spam_handler_data.get_by_sender(db, sender_email=sender_email, limit=limit)


@router.get("/{entry_id}", response_model=SpamHandlerDataResponse)
def get_spam_handler_data_entry(entry_id: int, db: Session = Depends(get_db)):
    """
    Get a single spam handler data entry by ID
    """
    db_entry = spam_handler_data.get(db, id=entry_id)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Spam handler data entry not found")
    return db_entry


@router.post("/", response_model=SpamHandlerDataResponse)
def create_spam_handler_data_entry(
    entry_in: SpamHandlerDataCreate, db: Session = Depends(get_db)
):
    """
    Create a new spam handler data entry
    """
    return spam_handler_data.create(db, obj_in=entry_in)


@router.post("/bulk", response_model=List[SpamHandlerDataResponse])
def bulk_create_spam_handler_data(
    bulk_data: SpamHandlerDataBulkCreate, db: Session = Depends(get_db)
):
    """
    Bulk create spam handler data entries
    """
    return spam_handler_data.bulk_create(db, objs_in=bulk_data.data_entries)


@router.put("/{entry_id}", response_model=SpamHandlerDataResponse)
def update_spam_handler_data_entry(
    entry_id: int, entry_update: SpamHandlerDataUpdate, db: Session = Depends(get_db)
):
    """
    Update a spam handler data entry
    """
    db_entry = spam_handler_data.get(db, id=entry_id)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Spam handler data entry not found")

    return spam_handler_data.update(db, db_obj=db_entry, obj_in=entry_update)


@router.delete("/{entry_id}", response_model=SpamHandlerDataResponse)
def delete_spam_handler_data_entry(entry_id: int, db: Session = Depends(get_db)):
    """
    Delete a single spam handler data entry
    """
    db_entry = spam_handler_data.remove(db, id=entry_id)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Spam handler data entry not found")
    return db_entry


@router.delete("/bulk/delete")
def bulk_delete_spam_handler_data(
    bulk_data: SpamHandlerDataBulkDelete, db: Session = Depends(get_db)
):
    """
    Bulk delete spam handler data entries
    """
    deleted_count = spam_handler_data.bulk_delete(db, ids=bulk_data.entry_ids)
    return {
        "message": f"Deleted {deleted_count} spam handler data entries",
        "deleted_count": deleted_count,
    }


@router.delete("/cleanup/old")
def cleanup_old_spam_handler_data(
    db: Session = Depends(get_db),
    days_old: int = Query(
        30, ge=1, le=365, description="Delete entries older than this many days"
    ),
):
    """
    Delete spam handler data entries older than specified days
    """
    deleted_count = spam_handler_data.delete_old_entries(db, days_old=days_old)
    return {
        "message": f"Deleted {deleted_count} old spam handler data entries",
        "deleted_count": deleted_count,
    }


@router.get("/export/csv")
def export_spam_handler_data_csv(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(None, description="Start date for export"),
    end_date: Optional[datetime] = Query(None, description="End date for export"),
    agent_name: Optional[str] = Query(None, description="Filter by agent name"),
    profile_name: Optional[str] = Query(None, description="Filter by profile name"),
):
    """
    Export spam handler data as CSV (returns download info)
    """
    # Get filtered data
    items, total = spam_handler_data.get_multi(
        db,
        skip=0,
        limit=10000,  # Large limit for export
        agent_name=agent_name,
        profile_name=profile_name,
        start_date=start_date,
        end_date=end_date,
    )

    return {
        "message": f"Export ready with {total} entries",
        "total_entries": total,
        "filters_applied": {
            "agent_name": agent_name,
            "profile_name": profile_name,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
        },
    }
