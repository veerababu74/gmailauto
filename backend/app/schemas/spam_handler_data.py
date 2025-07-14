from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime


class SpamHandlerDataBase(BaseModel):
    """Base schema for spam handler data"""

    agent_name: str
    profile_name: str
    sender_email: str
    spam_emails_found: int = 0
    moved_to_inbox: int = 0
    total_time_seconds: float = 0.0
    error_occurred: bool = False
    error_details: Optional[str] = None
    timestamp: Optional[datetime] = None
    spam_email_subjects: Optional[List[str]] = None

    @validator("spam_emails_found", "moved_to_inbox")
    def validate_non_negative_integers(cls, v):
        if v < 0:
            raise ValueError("Value must be non-negative")
        return v

    @validator("total_time_seconds")
    def validate_non_negative_float(cls, v):
        if v < 0:
            raise ValueError("Time must be non-negative")
        return v


class SpamHandlerDataCreate(SpamHandlerDataBase):
    """Schema for creating new spam handler data"""

    pass


class SpamHandlerDataUpdate(BaseModel):
    """Schema for updating spam handler data"""

    agent_name: Optional[str] = None
    profile_name: Optional[str] = None
    sender_email: Optional[str] = None
    spam_emails_found: Optional[int] = None
    moved_to_inbox: Optional[int] = None
    total_time_seconds: Optional[float] = None
    error_occurred: Optional[bool] = None
    error_details: Optional[str] = None
    spam_email_subjects: Optional[List[str]] = None


class SpamHandlerDataInDB(SpamHandlerDataBase):
    """Schema for spam handler data in database"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SpamHandlerDataResponse(SpamHandlerDataInDB):
    """Schema for spam handler data response"""

    pass


class SpamHandlerDataListResponse(BaseModel):
    """Schema for paginated spam handler data list response"""

    items: List[SpamHandlerDataResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class SpamHandlerDataBulkCreate(BaseModel):
    """Schema for bulk creating spam handler data"""

    data_entries: List[SpamHandlerDataCreate]


class SpamHandlerDataBulkDelete(BaseModel):
    """Schema for bulk deleting spam handler data"""

    entry_ids: List[int]


class SpamHandlerDataStats(BaseModel):
    """Schema for spam handler statistics"""

    total_operations: int
    total_spam_found: int
    total_moved_to_inbox: int
    average_processing_time: float
    success_rate: float
    error_rate: float
    top_senders: List[dict]
    operations_by_agent: List[dict]
    operations_by_profile: List[dict]


class SpamHandlerDataDateRange(BaseModel):
    """Schema for date range filtering"""

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
