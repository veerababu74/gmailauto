from pydantic import BaseModel, validator
from typing import Optional
from app.utils.email_validator import validate_email, EmailStr
from datetime import datetime


class DefaultSenderBase(BaseModel):
    """Base schema for default sender"""

    email: EmailStr
    description: Optional[str] = None
    is_active: bool = True

    @validator("email")
    def validate_email_field(cls, v):
        return validate_email(v)


class DefaultSenderCreate(DefaultSenderBase):
    """Schema for creating a new default sender"""

    pass


class DefaultSenderUpdate(BaseModel):
    """Schema for updating a default sender"""

    email: Optional[EmailStr] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class DefaultSenderInDB(DefaultSenderBase):
    """Schema for default sender in database"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class DefaultSenderResponse(DefaultSenderInDB):
    """Schema for default sender response"""

    pass


class DefaultSenderListResponse(BaseModel):
    """Schema for paginated default sender list response"""

    items: list[DefaultSenderResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class DefaultSenderBulkCreate(BaseModel):
    """Schema for bulk creating default senders"""

    senders: list[DefaultSenderCreate]


class DefaultSenderBulkDelete(BaseModel):
    """Schema for bulk deleting default senders"""

    sender_ids: list[int]
