from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime, timedelta
import math

from app.models.logged_out_profile import LoggedOutProfile
from app.schemas.logged_out_profile import (
    LoggedOutProfileCreate,
    LoggedOutProfileUpdate,
)


class CRUDLoggedOutProfile:
    """CRUD operations for Logged Out Profile"""

    def create(
        self, db: Session, *, obj_in: LoggedOutProfileCreate
    ) -> LoggedOutProfile:
        """Create a new logged out profile record"""
        db_obj = LoggedOutProfile(
            agent_name=obj_in.agent_name,
            profile_name=obj_in.profile_name,
            timestamp=datetime.utcnow(),  # Auto-generate timestamp
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[LoggedOutProfile]:
        """Get a logged out profile by ID"""
        return db.query(LoggedOutProfile).filter(LoggedOutProfile.id == id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: Optional[int] = 100,
        agent_name: Optional[str] = None,
        profile_name: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        search: Optional[str] = None,
    ) -> tuple[List[LoggedOutProfile], int]:
        """Get multiple logged out profiles with filtering and pagination"""
        query = db.query(LoggedOutProfile)

        # Apply filters
        if agent_name:
            query = query.filter(LoggedOutProfile.agent_name.ilike(f"%{agent_name}%"))

        if profile_name:
            query = query.filter(
                LoggedOutProfile.profile_name.ilike(f"%{profile_name}%")
            )

        if date_from:
            query = query.filter(LoggedOutProfile.timestamp >= date_from)

        if date_to:
            query = query.filter(LoggedOutProfile.timestamp <= date_to)

        if search:
            query = query.filter(
                or_(
                    LoggedOutProfile.agent_name.ilike(f"%{search}%"),
                    LoggedOutProfile.profile_name.ilike(f"%{search}%"),
                )
            )

        # Get total count before pagination
        total = query.count()

        # Apply pagination and ordering (newest first)
        if limit is not None:
            items = (
                query.order_by(desc(LoggedOutProfile.timestamp))
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            items = query.order_by(desc(LoggedOutProfile.timestamp)).offset(skip).all()

        return items, total

    def update(
        self, db: Session, *, db_obj: LoggedOutProfile, obj_in: LoggedOutProfileUpdate
    ) -> LoggedOutProfile:
        """Update a logged out profile"""
        update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> LoggedOutProfile:
        """Delete a logged out profile"""
        obj = db.query(LoggedOutProfile).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def get_by_agent_and_profile(
        self, db: Session, agent_name: str, profile_name: str
    ) -> List[LoggedOutProfile]:
        """Get logged out profiles by agent name and profile name"""
        return (
            db.query(LoggedOutProfile)
            .filter(
                and_(
                    LoggedOutProfile.agent_name == agent_name,
                    LoggedOutProfile.profile_name == profile_name,
                )
            )
            .order_by(desc(LoggedOutProfile.timestamp))
            .all()
        )

    def get_recent_by_agent(
        self, db: Session, agent_name: str, hours: int = 24
    ) -> List[LoggedOutProfile]:
        """Get recent logged out profiles for an agent within specified hours"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return (
            db.query(LoggedOutProfile)
            .filter(
                and_(
                    LoggedOutProfile.agent_name == agent_name,
                    LoggedOutProfile.timestamp >= cutoff_time,
                )
            )
            .order_by(desc(LoggedOutProfile.timestamp))
            .all()
        )

    def bulk_delete(self, db: Session, *, ids: List[int]) -> tuple[int, List[int]]:
        """Bulk delete logged out profiles by IDs"""
        deleted_count = 0
        failed_ids = []

        for id in ids:
            obj = db.query(LoggedOutProfile).get(id)
            if obj:
                db.delete(obj)
                deleted_count += 1
            else:
                failed_ids.append(id)

        db.commit()
        return deleted_count, failed_ids

    def get_analytics(
        self,
        db: Session,
        *,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        agent_name: Optional[str] = None,
    ) -> dict:
        """Get analytics for logged out profiles"""
        query = db.query(LoggedOutProfile)

        # Apply filters
        if date_from:
            query = query.filter(LoggedOutProfile.timestamp >= date_from)
        if date_to:
            query = query.filter(LoggedOutProfile.timestamp <= date_to)
        if agent_name:
            query = query.filter(LoggedOutProfile.agent_name == agent_name)

        total_logouts = query.count()

        # Get agent statistics
        agent_stats = (
            db.query(
                LoggedOutProfile.agent_name,
                db.func.count(LoggedOutProfile.id).label("logout_count"),
            )
            .filter(
                *[
                    condition
                    for condition in [
                        LoggedOutProfile.timestamp >= date_from if date_from else None,
                        LoggedOutProfile.timestamp <= date_to if date_to else None,
                        (
                            LoggedOutProfile.agent_name == agent_name
                            if agent_name
                            else None
                        ),
                    ]
                    if condition is not None
                ]
            )
            .group_by(LoggedOutProfile.agent_name)
            .order_by(db.func.count(LoggedOutProfile.id).desc())
            .limit(10)
            .all()
        )

        # Get profile statistics
        profile_stats = (
            db.query(
                LoggedOutProfile.profile_name,
                db.func.count(LoggedOutProfile.id).label("logout_count"),
            )
            .filter(
                *[
                    condition
                    for condition in [
                        LoggedOutProfile.timestamp >= date_from if date_from else None,
                        LoggedOutProfile.timestamp <= date_to if date_to else None,
                        (
                            LoggedOutProfile.agent_name == agent_name
                            if agent_name
                            else None
                        ),
                    ]
                    if condition is not None
                ]
            )
            .group_by(LoggedOutProfile.profile_name)
            .order_by(db.func.count(LoggedOutProfile.id).desc())
            .limit(10)
            .all()
        )

        return {
            "total_logouts": total_logouts,
            "top_agents": [
                {"agent_name": stat.agent_name, "logout_count": stat.logout_count}
                for stat in agent_stats
            ],
            "top_profiles": [
                {"profile_name": stat.profile_name, "logout_count": stat.logout_count}
                for stat in profile_stats
            ],
        }


# Create instance
logged_out_profile = CRUDLoggedOutProfile()
