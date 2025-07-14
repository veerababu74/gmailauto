from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum


class ClientStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    BLOCKED = "blocked"


class ClientBase(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    phone: Optional[str] = None
    status: ClientStatus = ClientStatus.ACTIVE
    notes: Optional[str] = None
    tags: Optional[List[str]] = []


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[ClientStatus] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class ClientInDB(ClientBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Client(ClientBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ClientStats(BaseModel):
    total_clients: int
    active_clients: int
    inactive_clients: int
    pending_clients: int
    blocked_clients: int
