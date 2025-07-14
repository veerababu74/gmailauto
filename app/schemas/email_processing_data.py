from pydantic import BaseModel, validator, HttpUrl
from typing import Optional, List
from datetime import datetime


class EmailProcessingDataBase(BaseModel):
    """Base schema for email processing data"""

    agent_name: str
    profile_name: str
    sender_email: str
    email_subject: str
    is_opened: bool = False
    is_link_clicked: bool = False
    is_unsubscribe_clicked: bool = False
    is_reply_sent: bool = False
    random_website_visited: Optional[str] = None
    random_website_duration_seconds: float = 0.0
    total_duration_seconds: float = 0.0
    error_occurred: bool = False
    error_details: Optional[str] = None
    timestamp: Optional[datetime] = None

    @validator("random_website_duration_seconds", "total_duration_seconds")
    def validate_non_negative_duration(cls, v):
        if v < 0:
            raise ValueError("Duration must be non-negative")
        return v

    @validator("email_subject")
    def validate_subject_length(cls, v):
        if len(v.strip()) == 0:
            raise ValueError("Email subject cannot be empty")
        return v.strip()


class EmailProcessingDataCreate(EmailProcessingDataBase):
    """Schema for creating new email processing data"""

    pass


class EmailProcessingDataUpdate(BaseModel):
    """Schema for updating email processing data"""

    agent_name: Optional[str] = None
    profile_name: Optional[str] = None
    sender_email: Optional[str] = None
    email_subject: Optional[str] = None
    is_opened: Optional[bool] = None
    is_link_clicked: Optional[bool] = None
    is_unsubscribe_clicked: Optional[bool] = None
    is_reply_sent: Optional[bool] = None
    random_website_visited: Optional[str] = None
    random_website_duration_seconds: Optional[float] = None
    total_duration_seconds: Optional[float] = None
    error_occurred: Optional[bool] = None
    error_details: Optional[str] = None


class EmailProcessingDataInDB(EmailProcessingDataBase):
    """Schema for email processing data in database"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EmailProcessingDataResponse(EmailProcessingDataInDB):
    """Schema for email processing data response"""

    pass


class EmailProcessingDataListResponse(BaseModel):
    """Schema for paginated email processing data list response"""

    items: List[EmailProcessingDataResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class EmailProcessingDataBulkCreate(BaseModel):
    """Schema for bulk creating email processing data"""

    data_entries: List[EmailProcessingDataCreate]


class EmailProcessingDataBulkDelete(BaseModel):
    """Schema for bulk deleting email processing data"""

    entry_ids: List[int]


class EmailProcessingDataStats(BaseModel):
    """Schema for email processing statistics"""

    total_emails_processed: int
    emails_opened: int
    links_clicked: int
    unsubscribe_clicked: int
    replies_sent: int
    average_processing_time: float
    average_website_duration: float
    success_rate: float
    error_rate: float
    top_senders: List[dict]
    processing_by_agent: List[dict]
    processing_by_profile: List[dict]
    website_visit_stats: List[dict]


class EmailProcessingDataDateRange(BaseModel):
    """Schema for date range filtering"""

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class EmailProcessingDataAnalytics(BaseModel):
    """Schema for email processing analytics"""

    open_rate: float
    click_rate: float
    unsubscribe_rate: float
    reply_rate: float
    error_rate: float
    avg_processing_time: float
    avg_website_time: float
    total_processed: int
