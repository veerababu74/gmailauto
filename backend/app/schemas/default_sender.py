from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime


class DefaultSenderBase(BaseModel):
    """Base schema for default sender"""

    email: EmailStr
    description: Optional[str] = None
    is_active: bool = True


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
        from_attributes = True


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
