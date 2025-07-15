from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class LoggedOutProfileBase(BaseModel):
    agent_name: str
    profile_name: str


class LoggedOutProfileCreate(LoggedOutProfileBase):
    pass


class LoggedOutProfileUpdate(BaseModel):
    agent_name: Optional[str] = None
    profile_name: Optional[str] = None


class LoggedOutProfileResponse(LoggedOutProfileBase):
    id: int
    timestamp: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LoggedOutProfileListResponse(BaseModel):
    items: list[LoggedOutProfileResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
