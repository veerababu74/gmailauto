from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

from app.core.database import Base


class ConnectivitySettings(Base):
    """Model for storing connectivity manager settings"""

    __tablename__ = "connectivity_settings"

    id = Column(Integer, primary_key=True, index=True)
    setting_name = Column(String(100), unique=True, index=True, nullable=False)
    setting_value = Column(String(500), nullable=False)
    setting_type = Column(
        String(50), nullable=False
    )  # 'boolean', 'integer', 'float', 'string', 'array'
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f"<ConnectivitySettings(id={self.id}, setting_name='{self.setting_name}', setting_value='{self.setting_value}', is_active={self.is_active})>"
