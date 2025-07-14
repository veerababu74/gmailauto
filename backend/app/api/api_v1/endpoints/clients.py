from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud import client
from app.schemas.client import (
    Client,
    ClientCreate,
    ClientUpdate,
    ClientStats,
    ClientStatus,
)
from app.schemas.user import User
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=List[Client])
def read_clients(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status_filter: ClientStatus = Query(None, alias="status"),
    search: str = Query(None),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve clients for current user
    """
    if search:
        clients = client.search(
            db, user_id=current_user.id, query=search, skip=skip, limit=limit
        )
    elif status_filter:
        clients = client.get_by_status(
            db, user_id=current_user.id, status=status_filter, skip=skip, limit=limit
        )
    else:
        clients = client.get_by_user(
            db, user_id=current_user.id, skip=skip, limit=limit
        )
    return clients


@router.post("/", response_model=Client)
def create_client(
    *,
    db: Session = Depends(get_db),
    client_in: ClientCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new client
    """
    # Check if client with this email already exists for this user
    existing_client = client.get_by_email(
        db, email=client_in.email, user_id=current_user.id
    )
    if existing_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client with this email already exists",
        )

    new_client = client.create_with_user(db, obj_in=client_in, user_id=current_user.id)
    return new_client


@router.get("/stats", response_model=ClientStats)
def read_client_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get client statistics for current user
    """
    stats = client.get_stats(db, user_id=current_user.id)
    return stats


@router.get("/{client_id}", response_model=Client)
def read_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get client by ID
    """
    client_obj = client.get(db, id=client_id)
    if not client_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    if client_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )
    return client_obj


@router.put("/{client_id}", response_model=Client)
def update_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
    client_in: ClientUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update client
    """
    client_obj = client.get(db, id=client_id)
    if not client_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    if client_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )
    updated_client = client.update(db, db_obj=client_obj, obj_in=client_in)
    return updated_client


@router.delete("/{client_id}")
def delete_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Delete client
    """
    client_obj = client.get(db, id=client_id)
    if not client_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    if client_obj.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )
    client.remove(db, id=client_id)
    return {"message": "Client deleted successfully"}
