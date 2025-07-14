from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

from app.core.database import Base


class RandomUrl(Base):
    """Model for storing random website URLs"""

    __tablename__ = "random_urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(2048), unique=True, index=True, nullable=False)
    description = Column(String(500), nullable=True)
    category = Column(
        String(100), nullable=True
    )  # e.g., 'social', 'news', 'shopping', etc.
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f"<RandomUrl(id={self.id}, url='{self.url}', category='{self.category}', is_active={self.is_active})>"
