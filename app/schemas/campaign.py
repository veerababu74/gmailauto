from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class CampaignType(str, Enum):
    OUTREACH = "outreach"
    FOLLOW_UP = "follow_up"
    NEWSLETTER = "newsletter"
    PROMOTIONAL = "promotional"


class CampaignBase(BaseModel):
    name: str
    subject: str
    content: str
    campaign_type: CampaignType = CampaignType.OUTREACH
    status: CampaignStatus = CampaignStatus.DRAFT
    scheduled_at: Optional[datetime] = None
    client_ids: Optional[List[int]] = []


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    campaign_type: Optional[CampaignType] = None
    status: Optional[CampaignStatus] = None
    scheduled_at: Optional[datetime] = None
    client_ids: Optional[List[int]] = None


class CampaignInDB(CampaignBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    sent_count: int = 0
    opened_count: int = 0
    replied_count: int = 0

    class Config:
        from_attributes = True


class Campaign(CampaignBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    sent_count: int = 0
    opened_count: int = 0
    replied_count: int = 0

    class Config:
        from_attributes = True


class CampaignStats(BaseModel):
    total_campaigns: int
    active_campaigns: int
    completed_campaigns: int
    draft_campaigns: int
    total_emails_sent: int
    total_opens: int
    total_replies: int
    open_rate: float
    reply_rate: float
