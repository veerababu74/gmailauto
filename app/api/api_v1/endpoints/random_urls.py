from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import math

from app.api.deps import get_db, get_current_user
from app.crud.crud_random_url import random_url
from app.schemas.random_url import (
    RandomUrlCreate,
    RandomUrlUpdate,
    RandomUrlResponse,
    RandomUrlListResponse,
    RandomUrlBulkCreate,
    RandomUrlBulkDelete,
    RandomUrlsByCategory,
)
from app.schemas.user import User

router = APIRouter()


@router.get("/", response_model=RandomUrlListResponse)
def get_random_urls(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(
        None, description="Search in URL, description, and category"
    ),
):
    """
    Get all random URLs with pagination and filtering
    """
    items, total = random_url.get_multi(
        db,
        skip=skip,
        limit=limit,
        is_active=is_active,
        category=category,
        search=search,
    )

    return RandomUrlListResponse(
        items=items,
        total=total,
        page=skip // limit + 1,
        per_page=limit,
        total_pages=math.ceil(total / limit) if total > 0 else 0,
    )


@router.get("/active", response_model=List[RandomUrlResponse])
def get_active_random_urls(db: Session = Depends(get_db)):
    """
    Get all active random URLs
    """
    return random_url.get_active(db)


@router.get("/urls", response_model=List[str])
def get_random_url_list(
    db: Session = Depends(get_db),
    is_active: bool = Query(True, description="Get active or inactive URLs"),
    category: Optional[str] = Query(None, description="Filter by category"),
):
    """
    Get list of random URLs only (for automation use)
    """
    return random_url.get_urls_list(db, is_active=is_active, category=category)


@router.get("/categories", response_model=List[str])
def get_url_categories(db: Session = Depends(get_db)):
    """
    Get all unique URL categories
    """
    return random_url.get_categories(db)


@router.get("/by-category/{category}", response_model=RandomUrlsByCategory)
def get_urls_by_category(category: str, db: Session = Depends(get_db)):
    """
    Get all URLs by category
    """
    urls = random_url.get_by_category(db, category)
    return RandomUrlsByCategory(category=category, urls=urls)


@router.get("/random", response_model=List[RandomUrlResponse])
def get_random_shuffled_urls(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100, description="Number of random URLs to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
):
    """
    Get random shuffled URLs (for automation use)
    """
    return random_url.get_random_urls(db, limit=limit, category=category)


@router.get("/{url_id}", response_model=RandomUrlResponse)
def get_random_url(url_id: int, db: Session = Depends(get_db)):
    """
    Get a single random URL by ID
    """
    db_url = random_url.get(db, id=url_id)
    if not db_url:
        raise HTTPException(status_code=404, detail="Random URL not found")
    return db_url


@router.post("/", response_model=RandomUrlResponse)
def create_random_url(
    url_in: RandomUrlCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new random URL
    """
    # Check if URL already exists
    existing_url = random_url.get_by_url(db, str(url_in.url))
    if existing_url:
        raise HTTPException(
            status_code=400, detail="A random URL with this address already exists"
        )

    return random_url.create(db, obj_in=url_in)


@router.post("/bulk", response_model=List[RandomUrlResponse])
def bulk_create_random_urls(
    bulk_data: RandomUrlBulkCreate, db: Session = Depends(get_db)
):
    """
    Bulk create random URLs
    """
    return random_url.bulk_create(db, objs_in=bulk_data.urls)


@router.put("/{url_id}", response_model=RandomUrlResponse)
def update_random_url(
    url_id: int, url_update: RandomUrlUpdate, db: Session = Depends(get_db)
):
    """
    Update a random URL
    """
    db_url = random_url.get(db, id=url_id)
    if not db_url:
        raise HTTPException(status_code=404, detail="Random URL not found")

    # Check if URL is being updated and if it already exists
    if url_update.url and str(url_update.url) != db_url.url:
        existing_url = random_url.get_by_url(db, str(url_update.url))
        if existing_url:
            raise HTTPException(
                status_code=400, detail="A random URL with this address already exists"
            )

    return random_url.update(db, db_obj=db_url, obj_in=url_update)


@router.delete("/{url_id}", response_model=RandomUrlResponse)
def delete_random_url(
    url_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a single random URL
    """
    db_url = random_url.remove(db, id=url_id)
    if not db_url:
        raise HTTPException(status_code=404, detail="Random URL not found")
    return db_url


@router.delete("/bulk/delete")
def bulk_delete_random_urls(
    bulk_data: RandomUrlBulkDelete, db: Session = Depends(get_db)
):
    """
    Bulk delete random URLs
    """
    deleted_count = random_url.bulk_delete(db, ids=bulk_data.url_ids)
    return {
        "message": f"Deleted {deleted_count} random URLs",
        "deleted_count": deleted_count,
    }


@router.delete("/")
def delete_all_random_urls(db: Session = Depends(get_db)):
    """
    Delete all random URLs
    """
    all_urls = random_url.get_multi(db, limit=10000)[0]  # Get all
    url_ids = [url.id for url in all_urls]
    deleted_count = random_url.bulk_delete(db, ids=url_ids)
    return {
        "message": f"Deleted all {deleted_count} random URLs",
        "deleted_count": deleted_count,
    }


@router.put("/activate/all")
def activate_all_random_urls(db: Session = Depends(get_db)):
    """
    Activate all random URLs
    """
    updated_count = random_url.activate_all(db)
    return {
        "message": f"Activated {updated_count} random URLs",
        "updated_count": updated_count,
    }


@router.put("/deactivate/all")
def deactivate_all_random_urls(db: Session = Depends(get_db)):
    """
    Deactivate all random URLs
    """
    updated_count = random_url.deactivate_all(db)
    return {
        "message": f"Deactivated {updated_count} random URLs",
        "updated_count": updated_count,
    }
