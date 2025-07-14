"""
Logged Out Profile API
API endpoints for managing logged out profile records
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime
import math

from app.api.deps import get_db
from app.crud.crud_logged_out_profile import logged_out_profile
from app.schemas.logged_out_profile import (
    LoggedOutProfileCreate,
    LoggedOutProfileUpdate,
    LoggedOutProfileResponse,
    LoggedOutProfileListResponse,
)

# Initialize router
router = APIRouter(tags=["Logged Out Profiles"])


# Bulk Operation Schemas (reusing from main file)
from pydantic import BaseModel


class BulkDeleteRequest(BaseModel):
    ids: List[int]


class BulkDeleteResponse(BaseModel):
    deleted_count: int
    failed_ids: List[int] = []


# ================================
# LOGGED OUT PROFILE ENDPOINTS
# ================================


@router.post(
    "/", response_model=LoggedOutProfileResponse, status_code=status.HTTP_201_CREATED
)
async def create_logged_out_profile(
    logged_out_profile_data: LoggedOutProfileCreate,
    db: Session = Depends(get_db),
):
    """
    Create new logged out profile entry

    **Request Body:**
    ```json
    {
        "agent_name": "Agent_001",
        "profile_name": "profile_gmail_1"
    }
    ```

    **Response:**
    ```json
    {
        "id": 1,
        "agent_name": "Agent_001",
        "profile_name": "profile_gmail_1",
        "timestamp": "2025-07-13T10:30:00Z",
        "created_at": "2025-07-13T10:30:00Z",
        "updated_at": "2025-07-13T10:30:00Z"
    }
    ```

    **Note:** The timestamp is automatically generated when the data is posted.
    """
    return logged_out_profile.create(db, obj_in=logged_out_profile_data)


@router.get("/", response_model=LoggedOutProfileListResponse)
async def get_logged_out_profiles(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    agent_name: Optional[str] = Query(None, description="Filter by agent name"),
    profile_name: Optional[str] = Query(None, description="Filter by profile name"),
    date_from: Optional[datetime] = Query(
        None, description="Filter from date (ISO format)"
    ),
    date_to: Optional[datetime] = Query(
        None, description="Filter to date (ISO format)"
    ),
    search: Optional[str] = Query(
        None, description="Search in agent_name and profile_name"
    ),
):
    """
    Get logged out profiles with filtering and pagination

    **Query Parameters:**
    - skip: Number of records to skip (default: 0)
    - limit: Number of records to return (default: 100, max: 1000)
    - agent_name: Filter by agent name (optional)
    - profile_name: Filter by profile name (optional)
    - date_from: Filter from date in ISO format (optional)
    - date_to: Filter to date in ISO format (optional)
    - search: Search in agent_name and profile_name (optional)

    **Response:**
    ```json
    {
        "items": [
            {
                "id": 1,
                "agent_name": "Agent_001",
                "profile_name": "profile_gmail_1",
                "timestamp": "2025-07-13T10:30:00Z",
                "created_at": "2025-07-13T10:30:00Z",
                "updated_at": "2025-07-13T10:30:00Z"
            }
        ],
        "total": 1,
        "page": 1,
        "per_page": 100,
        "total_pages": 1
    }
    ```
    """
    items, total = logged_out_profile.get_multi(
        db,
        skip=skip,
        limit=limit,
        agent_name=agent_name,
        profile_name=profile_name,
        date_from=date_from,
        date_to=date_to,
        search=search,
    )

    total_pages = math.ceil(total / limit) if limit > 0 else 1
    current_page = (skip // limit) + 1 if limit > 0 else 1

    return LoggedOutProfileListResponse(
        items=items,
        total=total,
        page=current_page,
        per_page=limit,
        total_pages=total_pages,
    )


@router.get("/{logged_out_profile_id}", response_model=LoggedOutProfileResponse)
async def get_logged_out_profile(
    logged_out_profile_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific logged out profile by ID

    **Response:**
    ```json
    {
        "id": 1,
        "agent_name": "Agent_001",
        "profile_name": "profile_gmail_1",
        "timestamp": "2025-07-13T10:30:00Z",
        "created_at": "2025-07-13T10:30:00Z",
        "updated_at": "2025-07-13T10:30:00Z"
    }
    ```
    """
    logged_out_profile_obj = logged_out_profile.get(db, id=logged_out_profile_id)
    if not logged_out_profile_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Logged out profile not found"
        )
    return logged_out_profile_obj


@router.put("/{logged_out_profile_id}", response_model=LoggedOutProfileResponse)
async def update_logged_out_profile(
    logged_out_profile_id: int,
    logged_out_profile_update: LoggedOutProfileUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a logged out profile

    **Request Body:**
    ```json
    {
        "agent_name": "Agent_002",
        "profile_name": "profile_gmail_2"
    }
    ```

    **Response:**
    Returns the updated logged out profile record.
    """
    logged_out_profile_obj = logged_out_profile.get(db, id=logged_out_profile_id)
    if not logged_out_profile_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Logged out profile not found"
        )

    return logged_out_profile.update(
        db, db_obj=logged_out_profile_obj, obj_in=logged_out_profile_update
    )


@router.delete("/{logged_out_profile_id}", response_model=LoggedOutProfileResponse)
async def delete_logged_out_profile(
    logged_out_profile_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a logged out profile

    **Response:**
    Returns the deleted logged out profile record.
    """
    logged_out_profile_obj = logged_out_profile.get(db, id=logged_out_profile_id)
    if not logged_out_profile_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Logged out profile not found"
        )

    return logged_out_profile.remove(db, id=logged_out_profile_id)


@router.post("/bulk-delete", response_model=BulkDeleteResponse)
async def bulk_delete_logged_out_profiles(
    bulk_delete_request: BulkDeleteRequest,
    db: Session = Depends(get_db),
):
    """
    Bulk delete logged out profiles

    **Request Body:**
    ```json
    {
        "ids": [1, 2, 3, 4, 5]
    }
    ```

    **Response:**
    ```json
    {
        "deleted_count": 4,
        "failed_ids": [5]
    }
    ```
    """
    deleted_count, failed_ids = logged_out_profile.bulk_delete(
        db, ids=bulk_delete_request.ids
    )

    return BulkDeleteResponse(deleted_count=deleted_count, failed_ids=failed_ids)


@router.get("/agent/{agent_name}", response_model=List[LoggedOutProfileResponse])
async def get_logged_out_profiles_by_agent(
    agent_name: str,
    db: Session = Depends(get_db),
    profile_name: Optional[str] = Query(None, description="Filter by profile name"),
):
    """
    Get logged out profiles by agent name

    **Response:**
    ```json
    [
        {
            "id": 1,
            "agent_name": "Agent_001",
            "profile_name": "profile_gmail_1",
            "timestamp": "2025-07-13T10:30:00Z",
            "created_at": "2025-07-13T10:30:00Z",
            "updated_at": "2025-07-13T10:30:00Z"
        }
    ]
    ```
    """
    if profile_name:
        return logged_out_profile.get_by_agent_and_profile(
            db, agent_name=agent_name, profile_name=profile_name
        )
    else:
        items, _ = logged_out_profile.get_multi(
            db, skip=0, limit=None, agent_name=agent_name
        )
        return items


@router.get("/analytics/stats")
async def get_logged_out_profile_analytics(
    db: Session = Depends(get_db),
    date_from: Optional[datetime] = Query(
        None, description="Filter from date (ISO format)"
    ),
    date_to: Optional[datetime] = Query(
        None, description="Filter to date (ISO format)"
    ),
    agent_name: Optional[str] = Query(None, description="Filter by agent name"),
):
    """
    Get logged out profile analytics and statistics

    **Request Parameters:**
    - date_from: Filter from date in ISO format (optional)
    - date_to: Filter to date in ISO format (optional)
    - agent_name: Filter by agent name (optional)

    **Response:**
    ```json
    {
        "total_logouts": 150,
        "top_agents": [
            {"agent_name": "Agent_001", "logout_count": 50},
            {"agent_name": "Agent_002", "logout_count": 45}
        ],
        "top_profiles": [
            {"profile_name": "profile_gmail_1", "logout_count": 30},
            {"profile_name": "profile_gmail_2", "logout_count": 25}
        ]
    }
    ```
    """
    stats = logged_out_profile.get_analytics(
        db, date_from=date_from, date_to=date_to, agent_name=agent_name
    )
    return stats


# ================================
# HEALTH CHECK ENDPOINTS
# ================================


@router.get("/health/check")
async def logged_out_profile_health_check():
    """
    Health check endpoint for logged out profile APIs

    **Response:**
    ```json
    {
        "status": "healthy",
        "service": "Logged Out Profile API",
        "timestamp": "2025-07-13T10:30:00Z"
    }
    ```
    """
    return {
        "status": "healthy",
        "service": "Logged Out Profile API",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
