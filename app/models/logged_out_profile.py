from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.core.database import Base


class LoggedOutProfile(Base):
    """Model for storing logged out profile records"""

    __tablename__ = "logged_out_profiles"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(255), nullable=False, index=True)
    profile_name = Column(String(255), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f"<LoggedOutProfile(id={self.id}, agent_name='{self.agent_name}', profile_name='{self.profile_name}', timestamp='{self.timestamp}')>"
