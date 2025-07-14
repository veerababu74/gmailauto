from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, JSON
from datetime import datetime

from app.core.database import Base


class SpamHandlerData(Base):
    """Model for storing spam handler operation data"""

    __tablename__ = "spam_handler_data"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(255), nullable=False, index=True)
    profile_name = Column(String(255), nullable=False, index=True)
    sender_email = Column(String(255), nullable=False, index=True)
    spam_emails_found = Column(Integer, default=0, nullable=False)
    moved_to_inbox = Column(Integer, default=0, nullable=False)
    total_time_seconds = Column(Float, default=0.0, nullable=False)
    error_occurred = Column(Boolean, default=False, nullable=False)
    error_details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    spam_email_subjects = Column(
        JSON, nullable=True
    )  # Store list of email subjects as JSON
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f"<SpamHandlerData(id={self.id}, agent='{self.agent_name}', profile='{self.profile_name}', sender='{self.sender_email}', spam_found={self.spam_emails_found})>"
