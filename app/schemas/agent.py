from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AgentBase(BaseModel):
    agent_name: str
    machine_brand: str
    location: str
    is_active: bool = True


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    agent_name: Optional[str] = None
    machine_brand: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None


class AgentInDBBase(AgentBase):
    id: int
    registration_date: datetime
    registration_time: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Agent(AgentInDBBase):
    pass


class AgentInDB(AgentInDBBase):
    pass
