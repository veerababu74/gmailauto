from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Agent(Base):
    """Agent model for registered automation agents"""

    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(255), unique=True, index=True, nullable=False)
    machine_brand = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    registration_date = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    registration_time = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
