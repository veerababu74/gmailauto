from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import json

from app.models.connectivity_settings import ConnectivitySettings
from app.schemas.connectivity_settings import (
    ConnectivitySettingsCreate,
    ConnectivitySettingsUpdate,
)


class CRUDConnectivitySettings:
    """CRUD operations for Connectivity Settings"""

    def create(
        self, db: Session, *, obj_in: ConnectivitySettingsCreate
    ) -> ConnectivitySettings:
        """Create a new connectivity setting"""
        db_obj = ConnectivitySettings(
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

    def get(self, db: Session, id: int) -> Optional[ConnectivitySettings]:
        """Get a setting by ID"""
        return (
            db.query(ConnectivitySettings).filter(ConnectivitySettings.id == id).first()
        )

    def get_by_name(
        self, db: Session, setting_name: str
    ) -> Optional[ConnectivitySettings]:
        """Get a setting by name"""
        return (
            db.query(ConnectivitySettings)
            .filter(ConnectivitySettings.setting_name == setting_name.upper())
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
    ) -> tuple[List[ConnectivitySettings], int]:
        """Get multiple settings with filtering and pagination"""
        query = db.query(ConnectivitySettings)

        # Apply filters
        if is_active is not None:
            query = query.filter(ConnectivitySettings.is_active == is_active)

        if setting_type:
            query = query.filter(
                ConnectivitySettings.setting_type == setting_type.lower()
            )

        if search:
            query = query.filter(
                or_(
                    ConnectivitySettings.setting_name.ilike(f"%{search}%"),
                    ConnectivitySettings.description.ilike(f"%{search}%"),
                )
            )

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        items = query.offset(skip).limit(limit).all()

        return items, total

    def get_active(self, db: Session) -> List[ConnectivitySettings]:
        """Get all active settings"""
        return (
            db.query(ConnectivitySettings)
            .filter(ConnectivitySettings.is_active == True)
            .all()
        )

    def update(
        self,
        db: Session,
        *,
        db_obj: ConnectivitySettings,
        obj_in: ConnectivitySettingsUpdate,
    ) -> ConnectivitySettings:
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
    ) -> Optional[ConnectivitySettings]:
        """Update a setting by name"""
        db_obj = self.get_by_name(db, setting_name)
        if db_obj:
            db_obj.setting_value = setting_value
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[ConnectivitySettings]:
        """Delete a setting"""
        obj = db.query(ConnectivitySettings).get(id)
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
                elif setting.setting_type == "array":
                    config[setting.setting_name] = json.loads(setting.setting_value)
                else:
                    config[setting.setting_name] = setting.setting_value
            except (ValueError, AttributeError, json.JSONDecodeError):
                config[setting.setting_name] = setting.setting_value

        return config

    def bulk_update_settings(
        self,
        db: Session,
        *,
        settings_dict: Dict[str, Union[str, int, float, bool, List[str]]],
    ) -> List[ConnectivitySettings]:
        """Bulk update settings from dictionary"""
        updated_settings = []

        for setting_name, value in settings_dict.items():
            # Convert value to string for storage
            if isinstance(value, bool):
                str_value = str(value).lower()
                setting_type = "boolean"
            elif isinstance(value, int):
                str_value = str(value)
                setting_type = "integer"
            elif isinstance(value, float):
                str_value = str(value)
                setting_type = "float"
            elif isinstance(value, list):
                str_value = json.dumps(value)
                setting_type = "array"
            else:
                str_value = str(value)
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
                new_setting = ConnectivitySettings(
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

    def initialize_default_settings(self, db: Session) -> List[ConnectivitySettings]:
        """Initialize default settings if they don't exist"""
        default_settings = {
            "ENABLE_CONNECTIVITY_MANAGER": (
                "true",
                "boolean",
                "Enable or disable connectivity management",
            ),
            "CONNECTIVITY_CHECK_TIMEOUT": (
                "10",
                "integer",
                "Timeout for connectivity checks (seconds)",
            ),
            "CONNECTIVITY_MAX_RETRIES": (
                "3",
                "integer",
                "Maximum number of connectivity retry attempts",
            ),
            "CONNECTIVITY_RETRY_DELAY": (
                "30",
                "integer",
                "Delay between connectivity retries (seconds)",
            ),
            "CONNECTIVITY_CHECK_INTERVAL": (
                "60",
                "integer",
                "Interval between connectivity checks (seconds)",
            ),
            "CONNECTIVITY_MAX_WAIT_TIME": (
                "600",
                "integer",
                "Maximum wait time for connectivity (seconds)",
            ),
            "CONNECTIVITY_TEST_URLS": (
                json.dumps(
                    [
                        "https://www.google.com",
                        "https://www.cloudflare.com",
                        "https://www.github.com",
                        "https://httpbin.org/status/200",
                    ]
                ),
                "array",
                "URLs used for connectivity testing",
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
                new_setting = ConnectivitySettings(
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

    def update_test_urls(
        self, db: Session, *, urls: List[str]
    ) -> Optional[ConnectivitySettings]:
        """Update connectivity test URLs"""
        urls_json = json.dumps(urls)
        return self.update_by_name(
            db, setting_name="CONNECTIVITY_TEST_URLS", setting_value=urls_json
        )

    def get_test_urls(self, db: Session) -> List[str]:
        """Get connectivity test URLs as a list"""
        setting = self.get_by_name(db, "CONNECTIVITY_TEST_URLS")
        if setting:
            try:
                return json.loads(setting.setting_value)
            except json.JSONDecodeError:
                pass

        # Return default URLs if setting not found or invalid
        return [
            "https://www.google.com",
            "https://www.cloudflare.com",
            "https://www.github.com",
            "https://httpbin.org/status/200",
        ]


connectivity_settings = CRUDConnectivitySettings()
