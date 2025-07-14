from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class ClientStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    BLOCKED = "blocked"


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Basic Info
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)

    # Status and Settings
    status = Column(Enum(ClientStatus), default=ClientStatus.ACTIVE)
    tags = Column(Text, nullable=True)  # JSON string for tags
    notes = Column(Text, nullable=True)

    # Contact Info
    website = Column(String, nullable=True)
    address = Column(Text, nullable=True)

    # Automation Settings
    auto_reply_enabled = Column(Boolean, default=False)
    auto_reply_message = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_contact = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="clients")
    campaigns = relationship("ClientCampaign", back_populates="client")
