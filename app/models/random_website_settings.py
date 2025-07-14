from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from datetime import datetime

from app.core.database import Base


class RandomWebsiteSettings(Base):
    """Model for storing random website feature settings"""

    __tablename__ = "random_website_settings"

    id = Column(Integer, primary_key=True, index=True)
    setting_name = Column(String(100), unique=True, index=True, nullable=False)
    setting_value = Column(String(500), nullable=False)
    setting_type = Column(
        String(50), nullable=False
    )  # 'boolean', 'integer', 'float', 'string'
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f"<RandomWebsiteSettings(id={self.id}, setting_name='{self.setting_name}', setting_value='{self.setting_value}', is_active={self.is_active})>"
