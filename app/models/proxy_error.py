from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

from app.core.database import Base


class ProxyError(Base):
    """Model for storing proxy error logs"""

    __tablename__ = "proxy_errors"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(255), nullable=False, index=True)
    proxy = Column(String(255), nullable=False, index=True)
    error_details = Column(Text, nullable=False)
    profile_name = Column(String(255), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f"<ProxyError(id={self.id}, agent_name='{self.agent_name}', proxy='{self.proxy}', profile_name='{self.profile_name}')>"
