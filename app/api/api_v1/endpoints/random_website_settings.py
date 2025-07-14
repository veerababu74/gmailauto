from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import math

from app.api.deps import get_db, get_current_user
from app.crud.crud_random_website_settings import random_website_settings
from app.schemas.random_website_settings import (
    RandomWebsiteSettingsCreate,
    RandomWebsiteSettingsUpdate,
    RandomWebsiteSettingsResponse,
    RandomWebsiteSettingsListResponse,
    RandomWebsiteSettingsBulkUpdate,
    RandomWebsiteSettingsConfig,
)
from app.schemas.user import User

router = APIRouter()


@router.get("/", response_model=RandomWebsiteSettingsListResponse)
def get_random_website_settings(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    setting_type: Optional[str] = Query(None, description="Filter by setting type"),
    search: Optional[str] = Query(
        None, description="Search in setting name and description"
    ),
):
    """
    Get all random website settings with pagination and filtering
    """
    items, total = random_website_settings.get_multi(
        db,
        skip=skip,
        limit=limit,
        is_active=is_active,
        setting_type=setting_type,
        search=search,
    )

    return RandomWebsiteSettingsListResponse(
        items=items,
        total=total,
        page=skip // limit + 1,
        per_page=limit,
        total_pages=math.ceil(total / limit) if total > 0 else 0,
    )


@router.get("/active", response_model=List[RandomWebsiteSettingsResponse])
def get_active_random_website_settings(db: Session = Depends(get_db)):
    """
    Get all active random website settings
    """
    return random_website_settings.get_active(db)


@router.get("/config", response_model=Dict[str, Any])
def get_random_website_config(db: Session = Depends(get_db)):
    """
    Get random website configuration as a dictionary (for automation use)
    """
    return random_website_settings.get_config_dict(db)


@router.get("/config/structured", response_model=RandomWebsiteSettingsConfig)
def get_structured_random_website_config(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Get random website configuration as a structured object
    """
    config_dict = random_website_settings.get_config_dict(db)

    # Fill in defaults for missing values
    return RandomWebsiteSettingsConfig(
        ENABLE_RANDOM_WEBSITES=config_dict.get("ENABLE_RANDOM_WEBSITES", False),
        RANDOM_WEBSITE_MIN_DURATION=config_dict.get("RANDOM_WEBSITE_MIN_DURATION", 15),
        RANDOM_WEBSITE_MAX_DURATION=config_dict.get("RANDOM_WEBSITE_MAX_DURATION", 30),
        RANDOM_SITE_MIN_DURATION=config_dict.get("RANDOM_SITE_MIN_DURATION", 20),
        RANDOM_SITE_MAX_DURATION=config_dict.get("RANDOM_SITE_MAX_DURATION", 40),
        EMAIL_TAB_CLOSE_DURATION=config_dict.get("EMAIL_TAB_CLOSE_DURATION", 20),
        DEFAULT_TIMEOUT=config_dict.get("DEFAULT_TIMEOUT", 20),
        LINK_CLICK_WAIT=config_dict.get("LINK_CLICK_WAIT", 5),
    )


@router.get("/by-name/{setting_name}", response_model=RandomWebsiteSettingsResponse)
def get_random_website_setting_by_name(
    setting_name: str, db: Session = Depends(get_db)
):
    """
    Get a single random website setting by name
    """
    db_setting = random_website_settings.get_by_name(db, setting_name)
    if not db_setting:
        raise HTTPException(status_code=404, detail="Random website setting not found")
    return db_setting


@router.get("/{setting_id}", response_model=RandomWebsiteSettingsResponse)
def get_random_website_setting(setting_id: int, db: Session = Depends(get_db)):
    """
    Get a single random website setting by ID
    """
    db_setting = random_website_settings.get(db, id=setting_id)
    if not db_setting:
        raise HTTPException(status_code=404, detail="Random website setting not found")
    return db_setting


@router.post("/", response_model=RandomWebsiteSettingsResponse)
def create_random_website_setting(
    setting_in: RandomWebsiteSettingsCreate, db: Session = Depends(get_db)
):
    """
    Create a new random website setting
    """
    # Check if setting name already exists
    existing_setting = random_website_settings.get_by_name(db, setting_in.setting_name)
    if existing_setting:
        raise HTTPException(
            status_code=400, detail="A setting with this name already exists"
        )

    return random_website_settings.create(db, obj_in=setting_in)


@router.post("/initialize-defaults", response_model=List[RandomWebsiteSettingsResponse])
def initialize_default_settings(db: Session = Depends(get_db)):
    """
    Initialize default random website settings if they don't exist
    """
    return random_website_settings.initialize_default_settings(db)


@router.put("/{setting_id}", response_model=RandomWebsiteSettingsResponse)
def update_random_website_setting(
    setting_id: int,
    setting_update: RandomWebsiteSettingsUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a random website setting
    """
    db_setting = random_website_settings.get(db, id=setting_id)
    if not db_setting:
        raise HTTPException(status_code=404, detail="Random website setting not found")

    return random_website_settings.update(db, db_obj=db_setting, obj_in=setting_update)


@router.put("/by-name/{setting_name}")
def update_random_website_setting_by_name(
    setting_name: str,
    setting_value: str = Query(..., description="New setting value"),
    db: Session = Depends(get_db),
):
    """
    Update a random website setting by name
    """
    db_setting = random_website_settings.update_by_name(
        db, setting_name=setting_name, setting_value=setting_value
    )
    if not db_setting:
        raise HTTPException(status_code=404, detail="Random website setting not found")

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


@router.put("/bulk/update", response_model=List[RandomWebsiteSettingsResponse])
def bulk_update_random_website_settings(
    bulk_data: RandomWebsiteSettingsBulkUpdate, db: Session = Depends(get_db)
):
    """
    Bulk update random website settings
    """
    return random_website_settings.bulk_update_settings(
        db, settings_dict=bulk_data.settings
    )


@router.put("/config/update", response_model=RandomWebsiteSettingsConfig)
def update_random_website_config(
    config: RandomWebsiteSettingsConfig,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update complete random website configuration
    """
    # Convert config to dictionary
    settings_dict = config.dict()

    # Update settings
    random_website_settings.bulk_update_settings(db, settings_dict=settings_dict)

    # Return updated config
    return get_structured_random_website_config(db)


@router.delete("/{setting_id}", response_model=RandomWebsiteSettingsResponse)
def delete_random_website_setting(setting_id: int, db: Session = Depends(get_db)):
    """
    Delete a single random website setting
    """
    db_setting = random_website_settings.remove(db, id=setting_id)
    if not db_setting:
        raise HTTPException(status_code=404, detail="Random website setting not found")
    return db_setting


@router.post("/reset-to-defaults", response_model=List[RandomWebsiteSettingsResponse])
def reset_to_default_settings(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Reset all settings to default values
    """
    # Delete all existing settings first
    all_settings = random_website_settings.get_multi(db, limit=1000)[0]
    for setting in all_settings:
        random_website_settings.remove(db, id=setting.id)

    # Initialize defaults
    return random_website_settings.initialize_default_settings(db)
