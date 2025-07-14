from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import math
from datetime import datetime

from app.api.deps import get_db
from app.crud.crud_email_processing_data import email_processing_data
from app.schemas.email_processing_data import (
    EmailProcessingDataCreate,
    EmailProcessingDataUpdate,
    EmailProcessingDataResponse,
    EmailProcessingDataListResponse,
    EmailProcessingDataBulkCreate,
    EmailProcessingDataBulkDelete,
    EmailProcessingDataStats,
)

router = APIRouter()


@router.get("/", response_model=EmailProcessingDataListResponse)
def get_email_processing_data(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    agent_name: Optional[str] = Query(None, description="Filter by agent name"),
    profile_name: Optional[str] = Query(None, description="Filter by profile name"),
    sender_email: Optional[str] = Query(None, description="Filter by sender email"),
    is_opened: Optional[bool] = Query(None, description="Filter by opened status"),
    is_link_clicked: Optional[bool] = Query(
        None, description="Filter by link clicked status"
    ),
    is_unsubscribe_clicked: Optional[bool] = Query(
        None, description="Filter by unsubscribe clicked status"
    ),
    is_reply_sent: Optional[bool] = Query(
        None, description="Filter by reply sent status"
    ),
    error_occurred: Optional[bool] = Query(None, description="Filter by error status"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    search: Optional[str] = Query(None, description="Search in multiple fields"),
):
    """
    Get all email processing data entries with pagination and filtering
    """
    items, total = email_processing_data.get_multi(
        db,
        skip=skip,
        limit=limit,
        agent_name=agent_name,
        profile_name=profile_name,
        sender_email=sender_email,
        is_opened=is_opened,
        is_link_clicked=is_link_clicked,
        is_unsubscribe_clicked=is_unsubscribe_clicked,
        is_reply_sent=is_reply_sent,
        error_occurred=error_occurred,
        start_date=start_date,
        end_date=end_date,
        search=search,
    )

    return EmailProcessingDataListResponse(
        items=items,
        total=total,
        page=skip // limit + 1,
        per_page=limit,
        total_pages=math.ceil(total / limit) if total > 0 else 0,
    )


@router.get("/recent", response_model=List[EmailProcessingDataResponse])
def get_recent_email_processing_data(
    db: Session = Depends(get_db),
    hours: int = Query(24, ge=1, le=168, description="Number of hours to look back"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of entries to return"
    ),
):
    """
    Get recent email processing data entries within specified hours
    """
    return email_processing_data.get_recent_entries(db, hours=hours, limit=limit)


@router.get("/statistics", response_model=EmailProcessingDataStats)
def get_email_processing_statistics(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(
        None, description="Start date for statistics"
    ),
    end_date: Optional[datetime] = Query(None, description="End date for statistics"),
):
    """
    Get email processing statistics
    """
    stats = email_processing_data.get_statistics(
        db, start_date=start_date, end_date=end_date
    )
    return EmailProcessingDataStats(**stats)


@router.get("/by-agent/{agent_name}", response_model=List[EmailProcessingDataResponse])
def get_email_processing_data_by_agent(
    agent_name: str,
    db: Session = Depends(get_db),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of entries to return"
    ),
):
    """
    Get email processing data by agent name
    """
    return email_processing_data.get_by_agent(db, agent_name=agent_name, limit=limit)


@router.get(
    "/by-profile/{profile_name}", response_model=List[EmailProcessingDataResponse]
)
def get_email_processing_data_by_profile(
    profile_name: str,
    db: Session = Depends(get_db),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of entries to return"
    ),
):
    """
    Get email processing data by profile name
    """
    return email_processing_data.get_by_profile(
        db, profile_name=profile_name, limit=limit
    )


@router.get(
    "/by-sender/{sender_email}", response_model=List[EmailProcessingDataResponse]
)
def get_email_processing_data_by_sender(
    sender_email: str,
    db: Session = Depends(get_db),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of entries to return"
    ),
):
    """
    Get email processing data by sender email
    """
    return email_processing_data.get_by_sender(
        db, sender_email=sender_email, limit=limit
    )


@router.get("/analytics", response_model=dict)
def get_email_processing_analytics(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(
        None, description="Start date for analytics"
    ),
    end_date: Optional[datetime] = Query(None, description="End date for analytics"),
    agent_name: Optional[str] = Query(None, description="Filter by agent name"),
    profile_name: Optional[str] = Query(None, description="Filter by profile name"),
):
    """
    Get email processing analytics with rates and performance metrics
    """
    return email_processing_data.get_analytics(
        db,
        start_date=start_date,
        end_date=end_date,
        agent_name=agent_name,
        profile_name=profile_name,
    )


@router.get("/{entry_id}", response_model=EmailProcessingDataResponse)
def get_email_processing_data_entry(entry_id: int, db: Session = Depends(get_db)):
    """
    Get a single email processing data entry by ID
    """
    db_entry = email_processing_data.get(db, id=entry_id)
    if not db_entry:
        raise HTTPException(
            status_code=404, detail="Email processing data entry not found"
        )
    return db_entry


@router.post("/", response_model=EmailProcessingDataResponse)
def create_email_processing_data_entry(
    entry_in: EmailProcessingDataCreate, db: Session = Depends(get_db)
):
    """
    Create a new email processing data entry
    """
    return email_processing_data.create(db, obj_in=entry_in)


@router.post("/bulk", response_model=List[EmailProcessingDataResponse])
def bulk_create_email_processing_data(
    bulk_data: EmailProcessingDataBulkCreate, db: Session = Depends(get_db)
):
    """
    Bulk create email processing data entries
    """
    return email_processing_data.bulk_create(db, objs_in=bulk_data.data_entries)


@router.put("/{entry_id}", response_model=EmailProcessingDataResponse)
def update_email_processing_data_entry(
    entry_id: int,
    entry_update: EmailProcessingDataUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an email processing data entry
    """
    db_entry = email_processing_data.get(db, id=entry_id)
    if not db_entry:
        raise HTTPException(
            status_code=404, detail="Email processing data entry not found"
        )

    return email_processing_data.update(db, db_obj=db_entry, obj_in=entry_update)


@router.delete("/{entry_id}", response_model=EmailProcessingDataResponse)
def delete_email_processing_data_entry(entry_id: int, db: Session = Depends(get_db)):
    """
    Delete a single email processing data entry
    """
    db_entry = email_processing_data.remove(db, id=entry_id)
    if not db_entry:
        raise HTTPException(
            status_code=404, detail="Email processing data entry not found"
        )
    return db_entry


@router.delete("/bulk/delete")
def bulk_delete_email_processing_data(
    bulk_data: EmailProcessingDataBulkDelete, db: Session = Depends(get_db)
):
    """
    Bulk delete email processing data entries
    """
    deleted_count = email_processing_data.bulk_delete(db, ids=bulk_data.entry_ids)
    return {
        "message": f"Deleted {deleted_count} email processing data entries",
        "deleted_count": deleted_count,
    }


@router.delete("/cleanup/old")
def cleanup_old_email_processing_data(
    db: Session = Depends(get_db),
    days_old: int = Query(
        30, ge=1, le=365, description="Delete entries older than this many days"
    ),
):
    """
    Delete email processing data entries older than specified days
    """
    deleted_count = email_processing_data.delete_old_entries(db, days_old=days_old)
    return {
        "message": f"Deleted {deleted_count} old email processing data entries",
        "deleted_count": deleted_count,
    }


@router.get("/export/csv")
def export_email_processing_data_csv(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(None, description="Start date for export"),
    end_date: Optional[datetime] = Query(None, description="End date for export"),
    agent_name: Optional[str] = Query(None, description="Filter by agent name"),
    profile_name: Optional[str] = Query(None, description="Filter by profile name"),
    sender_email: Optional[str] = Query(None, description="Filter by sender email"),
):
    """
    Export email processing data as CSV (returns download info)
    """
    # Get filtered data
    items, total = email_processing_data.get_multi(
        db,
        skip=0,
        limit=10000,  # Large limit for export
        agent_name=agent_name,
        profile_name=profile_name,
        sender_email=sender_email,
        start_date=start_date,
        end_date=end_date,
    )

    return {
        "message": f"Export ready with {total} entries",
        "total_entries": total,
        "filters_applied": {
            "agent_name": agent_name,
            "profile_name": profile_name,
            "sender_email": sender_email,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
        },
    }


@router.get("/performance/summary")
def get_performance_summary(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(None, description="Start date for summary"),
    end_date: Optional[datetime] = Query(None, description="End date for summary"),
):
    """
    Get performance summary including success rates and processing times
    """
    return email_processing_data.get_performance_summary(
        db, start_date=start_date, end_date=end_date
    )


@router.get("/trends/daily")
def get_daily_trends(
    db: Session = Depends(get_db),
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    agent_name: Optional[str] = Query(None, description="Filter by agent name"),
):
    """
    Get daily processing trends over specified number of days
    """
    return email_processing_data.get_daily_trends(db, days=days, agent_name=agent_name)
