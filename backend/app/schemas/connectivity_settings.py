from pydantic import BaseModel, validator, HttpUrl
from typing import Optional, Union, Any, List
from datetime import datetime


class ConnectivitySettingsBase(BaseModel):
    """Base schema for connectivity settings"""

    setting_name: str
    setting_value: str
    setting_type: str
    description: Optional[str] = None
    is_active: bool = True

    @validator("setting_type")
    def validate_setting_type(cls, v):
        allowed_types = ["boolean", "integer", "float", "string", "array"]
        if v.lower() not in allowed_types:
            raise ValueError(f'Setting type must be one of: {", ".join(allowed_types)}')
        return v.lower()

    @validator("setting_name")
    def validate_setting_name(cls, v):
        allowed_settings = [
            "ENABLE_CONNECTIVITY_MANAGER",
            "CONNECTIVITY_CHECK_TIMEOUT",
            "CONNECTIVITY_MAX_RETRIES",
            "CONNECTIVITY_RETRY_DELAY",
            "CONNECTIVITY_CHECK_INTERVAL",
            "CONNECTIVITY_MAX_WAIT_TIME",
            "CONNECTIVITY_TEST_URLS",
        ]
        if v.upper() not in allowed_settings:
            raise ValueError(
                f'Setting name must be one of: {", ".join(allowed_settings)}'
            )
        return v.upper()


class ConnectivitySettingsCreate(ConnectivitySettingsBase):
    """Schema for creating new connectivity settings"""

    pass


class ConnectivitySettingsUpdate(BaseModel):
    """Schema for updating connectivity settings"""

    setting_value: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ConnectivitySettingsInDB(ConnectivitySettingsBase):
    """Schema for connectivity settings in database"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ConnectivitySettingsResponse(ConnectivitySettingsInDB):
    """Schema for connectivity settings response"""

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
            elif self.setting_type == "array":
                import json

                self.parsed_value = json.loads(self.setting_value)
            else:
                self.parsed_value = self.setting_value
        except (ValueError, AttributeError, json.JSONDecodeError):
            self.parsed_value = self.setting_value

    parsed_value: Any = None


class ConnectivitySettingsListResponse(BaseModel):
    """Schema for paginated connectivity settings list response"""

    items: list[ConnectivitySettingsResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class ConnectivitySettingsBulkUpdate(BaseModel):
    """Schema for bulk updating connectivity settings"""

    settings: dict[str, Union[str, int, float, bool, List[str]]]


class ConnectivitySettingsConfig(BaseModel):
    """Schema for complete connectivity configuration"""

    ENABLE_CONNECTIVITY_MANAGER: bool = True
    CONNECTIVITY_CHECK_TIMEOUT: int = 10
    CONNECTIVITY_MAX_RETRIES: int = 3
    CONNECTIVITY_RETRY_DELAY: int = 30
    CONNECTIVITY_CHECK_INTERVAL: int = 60
    CONNECTIVITY_MAX_WAIT_TIME: int = 600
    CONNECTIVITY_TEST_URLS: List[str] = [
        "https://www.google.com",
        "https://www.cloudflare.com",
        "https://www.github.com",
        "https://httpbin.org/status/200",
    ]


class ConnectivityTestUrlCreate(BaseModel):
    """Schema for adding a test URL"""

    url: HttpUrl


class ConnectivityTestUrlsUpdate(BaseModel):
    """Schema for updating test URLs"""

    urls: List[HttpUrl]
