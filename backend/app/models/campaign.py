from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    Enum,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class CampaignType(str, enum.Enum):
    OUTREACH = "outreach"
    FOLLOW_UP = "follow_up"
    NEWSLETTER = "newsletter"
    PROMOTIONAL = "promotional"


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Campaign Info
    name = Column(String(255), nullable=False)
    subject = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    campaign_type = Column(Enum(CampaignType), default=CampaignType.OUTREACH)
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)

    # Email Content - removed html_body and renamed body to content

    # Scheduling
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Statistics - simplified to match schema
    sent_count = Column(Integer, default=0)
    opened_count = Column(Integer, default=0)
    replied_count = Column(Integer, default=0)

    # Settings - removed tracking settings for simplicity

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="campaigns")
    client_campaigns = relationship("ClientCampaign", back_populates="campaign")


class ClientCampaign(Base):
    __tablename__ = "client_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)

    # Individual tracking
    sent_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    opened_at = Column(DateTime(timezone=True), nullable=True)
    clicked_at = Column(DateTime(timezone=True), nullable=True)
    replied_at = Column(DateTime(timezone=True), nullable=True)
    bounced_at = Column(DateTime(timezone=True), nullable=True)

    # Status for this specific client
    status = Column(
        String(50), default="pending"
    )  # pending, sent, delivered, opened, clicked, replied, bounced

    # Relationships
    client = relationship("Client", back_populates="campaigns")
    campaign = relationship("Campaign", back_populates="client_campaigns")
