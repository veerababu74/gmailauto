from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import math

from app.api.deps import get_db, get_current_user
from app.crud.crud_proxy_error import proxy_error
from app.schemas.proxy_error import ProxyErrorCreate, ProxyErrorUpdate, ProxyError
from app.schemas.user import User

router = APIRouter()


class ProxyErrorListResponse(BaseModel):
    """Response schema for paginated proxy error list"""

    items: List[ProxyError]
    total: int
    page: int
    per_page: int
    total_pages: int


class ProxyErrorStatsResponse(BaseModel):
    """Response schema for proxy error statistics"""

    total_errors: int
    unique_agents: List[str]
    unique_proxies: List[str]
    unique_profiles: List[str]


@router.post("/", response_model=ProxyError, status_code=status.HTTP_201_CREATED)
def create_proxy_error(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    proxy_error_in: ProxyErrorCreate,
) -> ProxyError:
    """
    Create a new proxy error record.
    """
    return proxy_error.create(db=db, obj_in=proxy_error_in)


@router.get("/", response_model=ProxyErrorListResponse)
def read_proxy_errors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    agent_name: Optional[str] = Query(None, description="Filter by agent name"),
    proxy: Optional[str] = Query(None, description="Filter by proxy"),
    profile_name: Optional[str] = Query(None, description="Filter by profile name"),
    search: Optional[str] = Query(None, description="Search in all text fields"),
) -> ProxyErrorListResponse:
    """
    Retrieve proxy errors with filtering and pagination.
    """
    items, total = proxy_error.get_multi(
        db=db,
        skip=skip,
        limit=limit,
        agent_name=agent_name,
        proxy=proxy,
        profile_name=profile_name,
        search=search,
    )

    page = (skip // limit) + 1
    total_pages = math.ceil(total / limit) if total > 0 else 1

    return ProxyErrorListResponse(
        items=items,
        total=total,
        page=page,
        per_page=limit,
        total_pages=total_pages,
    )


@router.get("/stats", response_model=ProxyErrorStatsResponse)
def get_proxy_error_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProxyErrorStatsResponse:
    """
    Get proxy error statistics including unique values.
    """
    # Get total count
    _, total_errors = proxy_error.get_multi(db=db, skip=0, limit=1)

    return ProxyErrorStatsResponse(
        total_errors=total_errors,
        unique_agents=proxy_error.get_unique_agents(db=db),
        unique_proxies=proxy_error.get_unique_proxies(db=db),
        unique_profiles=proxy_error.get_unique_profiles(db=db),
    )


@router.get("/{proxy_error_id}", response_model=ProxyError)
def read_proxy_error(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    proxy_error_id: int,
) -> ProxyError:
    """
    Get a specific proxy error by ID.
    """
    proxy_error_obj = proxy_error.get(db=db, id=proxy_error_id)
    if not proxy_error_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proxy error not found"
        )
    return proxy_error_obj


@router.put("/{proxy_error_id}", response_model=ProxyError)
def update_proxy_error(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    proxy_error_id: int,
    proxy_error_in: ProxyErrorUpdate,
) -> ProxyError:
    """
    Update a proxy error.
    """
    proxy_error_obj = proxy_error.get(db=db, id=proxy_error_id)
    if not proxy_error_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proxy error not found"
        )
    return proxy_error.update(db=db, db_obj=proxy_error_obj, obj_in=proxy_error_in)


@router.delete("/{proxy_error_id}", response_model=ProxyError)
def delete_proxy_error(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    proxy_error_id: int,
) -> ProxyError:
    """
    Delete a proxy error.
    """
    proxy_error_obj = proxy_error.get(db=db, id=proxy_error_id)
    if not proxy_error_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proxy error not found"
        )
    return proxy_error.remove(db=db, id=proxy_error_id)


@router.get("/agent/{agent_name}", response_model=List[ProxyError])
def get_proxy_errors_by_agent(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    agent_name: str,
    limit: int = Query(
        10, ge=1, le=100, description="Number of recent errors to return"
    ),
) -> List[ProxyError]:
    """
    Get recent proxy errors for a specific agent.
    """
    return proxy_error.get_recent_by_agent(db=db, agent_name=agent_name, limit=limit)


@router.get("/proxy/{proxy_address}/count")
def get_proxy_error_count(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    proxy_address: str,
) -> dict:
    """
    Get total error count for a specific proxy.
    """
    count = proxy_error.count_by_proxy(db=db, proxy=proxy_address)
    return {"proxy": proxy_address, "error_count": count}
