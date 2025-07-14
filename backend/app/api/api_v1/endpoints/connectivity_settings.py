from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import math

from app.api.deps import get_db, get_current_user
from app.crud.crud_connectivity_settings import connectivity_settings
from app.schemas.connectivity_settings import (
    ConnectivitySettingsCreate,
    ConnectivitySettingsUpdate,
    ConnectivitySettingsResponse,
    ConnectivitySettingsListResponse,
    ConnectivitySettingsBulkUpdate,
    ConnectivitySettingsConfig,
    ConnectivityTestUrlCreate,
    ConnectivityTestUrlsUpdate,
)
from app.schemas.user import User

router = APIRouter()


@router.get("/", response_model=ConnectivitySettingsListResponse)
def get_connectivity_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    setting_type: Optional[str] = Query(None, description="Filter by setting type"),
    search: Optional[str] = Query(
        None, description="Search in setting name and description"
    ),
):
    """
    Get all connectivity settings with pagination and filtering
    """
    items, total = connectivity_settings.get_multi(
        db,
        skip=skip,
        limit=limit,
        is_active=is_active,
        setting_type=setting_type,
        search=search,
    )

    return ConnectivitySettingsListResponse(
        items=items,
        total=total,
        page=skip // limit + 1,
        per_page=limit,
        total_pages=math.ceil(total / limit) if total > 0 else 0,
    )


@router.get("/active", response_model=List[ConnectivitySettingsResponse])
def get_active_connectivity_settings(db: Session = Depends(get_db)):
    """
    Get all active connectivity settings
    """
    return connectivity_settings.get_active(db)


@router.get("/config", response_model=Dict[str, Any])
def get_connectivity_config(db: Session = Depends(get_db)):
    """
    Get connectivity configuration as a dictionary (for automation use)
    """
    return connectivity_settings.get_config_dict(db)


@router.get("/config/structured", response_model=ConnectivitySettingsConfig)
def get_structured_connectivity_config(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Get connectivity configuration as a structured object
    """
    config_dict = connectivity_settings.get_config_dict(db)

    # Fill in defaults for missing values
    return ConnectivitySettingsConfig(
        ENABLE_CONNECTIVITY_MANAGER=config_dict.get(
            "ENABLE_CONNECTIVITY_MANAGER", True
        ),
        CONNECTIVITY_CHECK_TIMEOUT=config_dict.get("CONNECTIVITY_CHECK_TIMEOUT", 10),
        CONNECTIVITY_MAX_RETRIES=config_dict.get("CONNECTIVITY_MAX_RETRIES", 3),
        CONNECTIVITY_RETRY_DELAY=config_dict.get("CONNECTIVITY_RETRY_DELAY", 30),
        CONNECTIVITY_CHECK_INTERVAL=config_dict.get("CONNECTIVITY_CHECK_INTERVAL", 60),
        CONNECTIVITY_MAX_WAIT_TIME=config_dict.get("CONNECTIVITY_MAX_WAIT_TIME", 600),
        CONNECTIVITY_TEST_URLS=config_dict.get(
            "CONNECTIVITY_TEST_URLS",
            [
                "https://www.google.com",
                "https://www.cloudflare.com",
                "https://www.github.com",
                "https://httpbin.org/status/200",
            ],
        ),
    )


@router.get("/test-urls", response_model=List[str])
def get_connectivity_test_urls(db: Session = Depends(get_db)):
    """
    Get connectivity test URLs list
    """
    return connectivity_settings.get_test_urls(db)


@router.get("/by-name/{setting_name}", response_model=ConnectivitySettingsResponse)
def get_connectivity_setting_by_name(setting_name: str, db: Session = Depends(get_db)):
    """
    Get a single connectivity setting by name
    """
    db_setting = connectivity_settings.get_by_name(db, setting_name)
    if not db_setting:
        raise HTTPException(status_code=404, detail="Connectivity setting not found")
    return db_setting


@router.get("/{setting_id}", response_model=ConnectivitySettingsResponse)
def get_connectivity_setting(setting_id: int, db: Session = Depends(get_db)):
    """
    Get a single connectivity setting by ID
    """
    db_setting = connectivity_settings.get(db, id=setting_id)
    if not db_setting:
        raise HTTPException(status_code=404, detail="Connectivity setting not found")
    return db_setting


@router.post("/", response_model=ConnectivitySettingsResponse)
def create_connectivity_setting(
    setting_in: ConnectivitySettingsCreate, db: Session = Depends(get_db)
):
    """
    Create a new connectivity setting
    """
    # Check if setting name already exists
    existing_setting = connectivity_settings.get_by_name(db, setting_in.setting_name)
    if existing_setting:
        raise HTTPException(
            status_code=400, detail="A setting with this name already exists"
        )

    return connectivity_settings.create(db, obj_in=setting_in)


@router.post("/initialize-defaults", response_model=List[ConnectivitySettingsResponse])
def initialize_default_settings(db: Session = Depends(get_db)):
    """
    Initialize default connectivity settings if they don't exist
    """
    return connectivity_settings.initialize_default_settings(db)


@router.post("/test-urls", response_model=ConnectivitySettingsResponse)
def add_connectivity_test_url(
    url_data: ConnectivityTestUrlCreate, db: Session = Depends(get_db)
):
    """
    Add a new connectivity test URL
    """
    current_urls = connectivity_settings.get_test_urls(db)
    new_url = str(url_data.url)

    if new_url not in current_urls:
        current_urls.append(new_url)
        updated_setting = connectivity_settings.update_test_urls(db, urls=current_urls)
        if not updated_setting:
            raise HTTPException(status_code=500, detail="Failed to update test URLs")
        return updated_setting

    raise HTTPException(status_code=400, detail="URL already exists in test URLs")


@router.put("/{setting_id}", response_model=ConnectivitySettingsResponse)
def update_connectivity_setting(
    setting_id: int,
    setting_update: ConnectivitySettingsUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a connectivity setting
    """
    db_setting = connectivity_settings.get(db, id=setting_id)
    if not db_setting:
        raise HTTPException(status_code=404, detail="Connectivity setting not found")

    return connectivity_settings.update(db, db_obj=db_setting, obj_in=setting_update)


@router.put("/by-name/{setting_name}")
def update_connectivity_setting_by_name(
    setting_name: str,
    setting_value: str = Query(..., description="New setting value"),
    db: Session = Depends(get_db),
):
    """
    Update a connectivity setting by name
    """
    db_setting = connectivity_settings.update_by_name(
        db, setting_name=setting_name, setting_value=setting_value
    )
    if not db_setting:
        raise HTTPException(status_code=404, detail="Connectivity setting not found")

    # Return as dict to avoid validation issues
    return {
        "id": db_setting.id,
        "setting_name": db_setting.setting_name,
        "setting_value": db_setting.setting_value,
        "setting_type": db_setting.setting_type,
        "description": db_setting.description,
        "is_active": db_setting.is_active,
        "created_at": db_setting.created_at,
        "updated_at": db_setting.updated_at,
    }


@router.put("/bulk/update", response_model=List[ConnectivitySettingsResponse])
def bulk_update_connectivity_settings(
    bulk_data: ConnectivitySettingsBulkUpdate, db: Session = Depends(get_db)
):
    """
    Bulk update connectivity settings
    """
    return connectivity_settings.bulk_update_settings(
        db, settings_dict=bulk_data.settings
    )


@router.put("/config/update", response_model=ConnectivitySettingsConfig)
def update_connectivity_config(
    config: ConnectivitySettingsConfig,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update complete connectivity configuration
    """
    # Convert config to dictionary
    settings_dict = config.dict()

    # Update settings
    connectivity_settings.bulk_update_settings(db, settings_dict=settings_dict)

    # Return updated config
    return get_structured_connectivity_config(db)


@router.put("/test-urls/update", response_model=ConnectivitySettingsResponse)
def update_connectivity_test_urls(
    urls_data: ConnectivityTestUrlsUpdate, db: Session = Depends(get_db)
):
    """
    Update all connectivity test URLs
    """
    urls = [str(url) for url in urls_data.urls]
    updated_setting = connectivity_settings.update_test_urls(db, urls=urls)
    if not updated_setting:
        raise HTTPException(status_code=500, detail="Failed to update test URLs")
    return updated_setting


@router.delete("/{setting_id}", response_model=ConnectivitySettingsResponse)
def delete_connectivity_setting(setting_id: int, db: Session = Depends(get_db)):
    """
    Delete a single connectivity setting
    """
    db_setting = connectivity_settings.remove(db, id=setting_id)
    if not db_setting:
        raise HTTPException(status_code=404, detail="Connectivity setting not found")
    return db_setting


@router.delete("/test-urls/{url}")
def remove_connectivity_test_url(url: str, db: Session = Depends(get_db)):
    """
    Remove a connectivity test URL
    """
    current_urls = connectivity_settings.get_test_urls(db)

    if url in current_urls:
        current_urls.remove(url)
        updated_setting = connectivity_settings.update_test_urls(db, urls=current_urls)
        if updated_setting:
            return {"message": f"Removed URL: {url}", "remaining_urls": current_urls}

    raise HTTPException(status_code=404, detail="URL not found in test URLs")


@router.post("/reset-to-defaults", response_model=List[ConnectivitySettingsResponse])
def reset_to_default_settings(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Reset all settings to default values
    """
    # Delete all existing settings first
    all_settings = connectivity_settings.get_multi(db, limit=1000)[0]
    for setting in all_settings:
        connectivity_settings.remove(db, id=setting.id)

    # Initialize defaults
    return connectivity_settings.initialize_default_settings(db)
