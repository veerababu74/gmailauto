from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import json

from app.models.random_website_settings import RandomWebsiteSettings
from app.schemas.random_website_settings import (
    RandomWebsiteSettingsCreate,
    RandomWebsiteSettingsUpdate,
)


class CRUDRandomWebsiteSettings:
    """CRUD operations for Random Website Settings"""

    def create(
        self, db: Session, *, obj_in: RandomWebsiteSettingsCreate
    ) -> RandomWebsiteSettings:
        """Create a new random website setting"""
        db_obj = RandomWebsiteSettings(
            setting_name=obj_in.setting_name,
            setting_value=obj_in.setting_value,
            setting_type=obj_in.setting_type,
            description=obj_in.description,
            is_active=obj_in.is_active,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[RandomWebsiteSettings]:
        """Get a setting by ID"""
        return (
            db.query(RandomWebsiteSettings)
            .filter(RandomWebsiteSettings.id == id)
            .first()
        )

    def get_by_name(
        self, db: Session, setting_name: str
    ) -> Optional[RandomWebsiteSettings]:
        """Get a setting by name"""
        return (
            db.query(RandomWebsiteSettings)
            .filter(RandomWebsiteSettings.setting_name == setting_name.upper())
            .first()
        )

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        setting_type: Optional[str] = None,
        search: Optional[str] = None,
    ) -> tuple[List[RandomWebsiteSettings], int]:
        """Get multiple settings with filtering and pagination"""
        query = db.query(RandomWebsiteSettings)

        # Apply filters
        if is_active is not None:
            query = query.filter(RandomWebsiteSettings.is_active == is_active)

        if setting_type:
            query = query.filter(
                RandomWebsiteSettings.setting_type == setting_type.lower()
            )

        if search:
            query = query.filter(
                or_(
                    RandomWebsiteSettings.setting_name.ilike(f"%{search}%"),
                    RandomWebsiteSettings.description.ilike(f"%{search}%"),
                )
            )

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        items = query.offset(skip).limit(limit).all()

        return items, total

    def get_active(self, db: Session) -> List[RandomWebsiteSettings]:
        """Get all active settings"""
        return (
            db.query(RandomWebsiteSettings)
            .filter(RandomWebsiteSettings.is_active == True)
            .all()
        )

    def update(
        self,
        db: Session,
        *,
        db_obj: RandomWebsiteSettings,
        obj_in: RandomWebsiteSettingsUpdate,
    ) -> RandomWebsiteSettings:
        """Update a setting"""
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_by_name(
        self, db: Session, *, setting_name: str, setting_value: str
    ) -> Optional[RandomWebsiteSettings]:
        """Update a setting by name"""
        db_obj = self.get_by_name(db, setting_name)
        if db_obj:
            db_obj.setting_value = setting_value
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[RandomWebsiteSettings]:
        """Delete a setting"""
        obj = db.query(RandomWebsiteSettings).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def get_config_dict(self, db: Session) -> Dict[str, Any]:
        """Get all settings as a configuration dictionary with parsed values"""
        settings = self.get_active(db)
        config = {}

        for setting in settings:
            try:
                if setting.setting_type == "boolean":
                    config[setting.setting_name] = setting.setting_value.lower() in (
                        "true",
                        "1",
                        "yes",
                        "on",
                    )
                elif setting.setting_type == "integer":
                    config[setting.setting_name] = int(setting.setting_value)
                elif setting.setting_type == "float":
                    config[setting.setting_name] = float(setting.setting_value)
                else:
                    config[setting.setting_name] = setting.setting_value
            except (ValueError, AttributeError):
                config[setting.setting_name] = setting.setting_value

        return config

    def bulk_update_settings(
        self, db: Session, *, settings_dict: Dict[str, Union[str, int, float, bool]]
    ) -> List[RandomWebsiteSettings]:
        """Bulk update settings from dictionary"""
        updated_settings = []

        for setting_name, value in settings_dict.items():
            # Convert value to string for storage
            str_value = str(value).lower() if isinstance(value, bool) else str(value)

            # Determine setting type
            if isinstance(value, bool):
                setting_type = "boolean"
            elif isinstance(value, int):
                setting_type = "integer"
            elif isinstance(value, float):
                setting_type = "float"
            else:
                setting_type = "string"

            # Check if setting exists
            existing = self.get_by_name(db, setting_name)
            if existing:
                existing.setting_value = str_value
                existing.setting_type = setting_type
                db.add(existing)
                updated_settings.append(existing)
            else:
                # Create new setting
                new_setting = RandomWebsiteSettings(
                    setting_name=setting_name.upper(),
                    setting_value=str_value,
                    setting_type=setting_type,
                    is_active=True,
                )
                db.add(new_setting)
                updated_settings.append(new_setting)

        db.commit()
        for setting in updated_settings:
            db.refresh(setting)

        return updated_settings

    def initialize_default_settings(self, db: Session) -> List[RandomWebsiteSettings]:
        """Initialize default settings if they don't exist"""
        default_settings = {
            "ENABLE_RANDOM_WEBSITES": (
                "false",
                "boolean",
                "Enable or disable random website browsing feature",
            ),
            "RANDOM_WEBSITE_MIN_DURATION": (
                "15",
                "integer",
                "Minimum duration for random website browsing (seconds)",
            ),
            "RANDOM_WEBSITE_MAX_DURATION": (
                "30",
                "integer",
                "Maximum duration for random website browsing (seconds)",
            ),
            "RANDOM_SITE_MIN_DURATION": (
                "20",
                "integer",
                "Minimum duration for random site visit (seconds)",
            ),
            "RANDOM_SITE_MAX_DURATION": (
                "40",
                "integer",
                "Maximum duration for random site visit (seconds)",
            ),
            "EMAIL_TAB_CLOSE_DURATION": (
                "20",
                "integer",
                "Duration before closing email tab (seconds)",
            ),
            "DEFAULT_TIMEOUT": (
                "20",
                "integer",
                "Default timeout for operations (seconds)",
            ),
            "LINK_CLICK_WAIT": (
                "5",
                "integer",
                "Wait time after clicking links (seconds)",
            ),
        }

        created_settings = []
        for setting_name, (
            default_value,
            setting_type,
            description,
        ) in default_settings.items():
            existing = self.get_by_name(db, setting_name)
            if not existing:
                new_setting = RandomWebsiteSettings(
                    setting_name=setting_name,
                    setting_value=default_value,
                    setting_type=setting_type,
                    description=description,
                    is_active=True,
                )
                db.add(new_setting)
                created_settings.append(new_setting)

        if created_settings:
            db.commit()
            for setting in created_settings:
                db.refresh(setting)

        return created_settings


random_website_settings = CRUDRandomWebsiteSettings()
