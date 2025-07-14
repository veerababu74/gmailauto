from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Profile fields
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)

    # Gmail integration
    gmail_token = Column(Text, nullable=True)
    gmail_refresh_token = Column(Text, nullable=True)
    gmail_connected = Column(Boolean, default=False)

    # Email verification and password reset
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    verification_token_expires = Column(DateTime(timezone=True), nullable=True)
    reset_password_token = Column(String, nullable=True)
    reset_password_token_expires = Column(DateTime(timezone=True), nullable=True)

    # Settings
    email_notifications = Column(Boolean, default=True)
    two_factor_enabled = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    clients = relationship("Client", back_populates="user")
    campaigns = relationship("Campaign", back_populates="user")
