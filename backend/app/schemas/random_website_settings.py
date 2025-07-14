from pydantic import BaseModel, validator
from typing import Optional, Union, Any
from datetime import datetime


class RandomWebsiteSettingsBase(BaseModel):
    """Base schema for random website settings"""

    setting_name: str
    setting_value: str
    setting_type: str
    description: Optional[str] = None
    is_active: bool = True

    @validator("setting_type")
    def validate_setting_type(cls, v):
        allowed_types = ["boolean", "integer", "float", "string"]
        if v.lower() not in allowed_types:
            raise ValueError(f'Setting type must be one of: {", ".join(allowed_types)}')
        return v.lower()

    @validator("setting_name")
    def validate_setting_name(cls, v):
        allowed_settings = [
            "ENABLE_RANDOM_WEBSITES",
            "RANDOM_WEBSITE_MIN_DURATION",
            "RANDOM_WEBSITE_MAX_DURATION",
            "RANDOM_SITE_MIN_DURATION",
            "RANDOM_SITE_MAX_DURATION",
            "EMAIL_TAB_CLOSE_DURATION",
            "DEFAULT_TIMEOUT",
            "LINK_CLICK_WAIT",
        ]
        if v.upper() not in allowed_settings:
            raise ValueError(
                f'Setting name must be one of: {", ".join(allowed_settings)}'
            )
        return v.upper()


class RandomWebsiteSettingsCreate(RandomWebsiteSettingsBase):
    """Schema for creating new random website settings"""

    pass


class RandomWebsiteSettingsUpdate(BaseModel):
    """Schema for updating random website settings"""

    setting_value: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class RandomWebsiteSettingsInDB(RandomWebsiteSettingsBase):
    """Schema for random website settings in database"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RandomWebsiteSettingsResponse(RandomWebsiteSettingsInDB):
    """Schema for random website settings response"""

    def __init__(self, **data):
        super().__init__(**data)
        # Calculate parsed_value based on setting_type and setting_value
        try:
            if self.setting_type == "boolean":
                self.parsed_value = self.setting_value.lower() in (
                    "true",
                    "1",
                    "yes",
                    "on",
                )
            elif self.setting_type == "integer":
                self.parsed_value = int(self.setting_value)
            elif self.setting_type == "float":
                self.parsed_value = float(self.setting_value)
            else:
                self.parsed_value = self.setting_value
        except (ValueError, AttributeError):
            self.parsed_value = self.setting_value

    parsed_value: Any = None


class RandomWebsiteSettingsListResponse(BaseModel):
    """Schema for paginated random website settings list response"""

    items: list[RandomWebsiteSettingsResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class RandomWebsiteSettingsBulkUpdate(BaseModel):
    """Schema for bulk updating random website settings"""

    settings: dict[str, Union[str, int, float, bool]]


class RandomWebsiteSettingsConfig(BaseModel):
    """Schema for complete random website configuration"""

    ENABLE_RANDOM_WEBSITES: bool = False
    RANDOM_WEBSITE_MIN_DURATION: int = 15
    RANDOM_WEBSITE_MAX_DURATION: int = 30
    RANDOM_SITE_MIN_DURATION: int = 20
    RANDOM_SITE_MAX_DURATION: int = 40
    EMAIL_TAB_CLOSE_DURATION: int = 20
    DEFAULT_TIMEOUT: int = 20
    LINK_CLICK_WAIT: int = 5
