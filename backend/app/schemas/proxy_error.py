from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ProxyErrorBase(BaseModel):
    agent_name: str
    proxy: str
    error_details: str
    profile_name: str


class ProxyErrorCreate(ProxyErrorBase):
    pass


class ProxyErrorUpdate(BaseModel):
    agent_name: Optional[str] = None
    proxy: Optional[str] = None
    error_details: Optional[str] = None
    profile_name: Optional[str] = None


class ProxyErrorInDB(ProxyErrorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProxyError(ProxyErrorInDB):
    pass
