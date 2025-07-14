from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text
from datetime import datetime

from app.core.database import Base


class EmailProcessingData(Base):
    """Model for storing email processing operation data"""

    __tablename__ = "email_processing_data"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(255), nullable=False, index=True)
    profile_name = Column(String(255), nullable=False, index=True)
    sender_email = Column(String(255), nullable=False, index=True)
    email_subject = Column(String(500), nullable=False)
    is_opened = Column(Boolean, default=False, nullable=False)
    is_link_clicked = Column(Boolean, default=False, nullable=False)
    is_unsubscribe_clicked = Column(Boolean, default=False, nullable=False)
    is_reply_sent = Column(Boolean, default=False, nullable=False)
    random_website_visited = Column(String(2048), nullable=True)
    random_website_duration_seconds = Column(Float, default=0.0, nullable=False)
    total_duration_seconds = Column(Float, default=0.0, nullable=False)
    error_occurred = Column(Boolean, default=False, nullable=False)
    error_details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f"<EmailProcessingData(id={self.id}, agent='{self.agent_name}', profile='{self.profile_name}', sender='{self.sender_email}', subject='{self.email_subject[:50]}...')>"
