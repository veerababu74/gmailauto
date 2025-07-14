from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from datetime import datetime, timedelta

from app.models.spam_handler_data import SpamHandlerData
from app.schemas.spam_handler_data import SpamHandlerDataCreate, SpamHandlerDataUpdate


class CRUDSpamHandlerData:
    """CRUD operations for Spam Handler Data"""

    def create(self, db: Session, *, obj_in: SpamHandlerDataCreate) -> SpamHandlerData:
        """Create a new spam handler data entry"""
        # Set timestamp if not provided
        timestamp = obj_in.timestamp or datetime.utcnow()

        db_obj = SpamHandlerData(
            agent_name=obj_in.agent_name,
            profile_name=obj_in.profile_name,
            sender_email=obj_in.sender_email,
            spam_emails_found=obj_in.spam_emails_found,
            moved_to_inbox=obj_in.moved_to_inbox,
            total_time_seconds=obj_in.total_time_seconds,
            error_occurred=obj_in.error_occurred,
            error_details=obj_in.error_details,
            timestamp=timestamp,
            spam_email_subjects=obj_in.spam_email_subjects or [],
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[SpamHandlerData]:
        """Get a spam handler data entry by ID"""
        return db.query(SpamHandlerData).filter(SpamHandlerData.id == id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        agent_name: Optional[str] = None,
        profile_name: Optional[str] = None,
        sender_email: Optional[str] = None,
        error_occurred: Optional[bool] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        search: Optional[str] = None,
    ) -> tuple[List[SpamHandlerData], int]:
        """Get multiple spam handler data entries with filtering and pagination"""
        query = db.query(SpamHandlerData)

        # Apply filters
        if agent_name:
            query = query.filter(SpamHandlerData.agent_name.ilike(f"%{agent_name}%"))

        if profile_name:
            query = query.filter(
                SpamHandlerData.profile_name.ilike(f"%{profile_name}%")
            )

        if sender_email:
            query = query.filter(
                SpamHandlerData.sender_email.ilike(f"%{sender_email}%")
            )

        if error_occurred is not None:
            query = query.filter(SpamHandlerData.error_occurred == error_occurred)

        if start_date:
            query = query.filter(SpamHandlerData.timestamp >= start_date)

        if end_date:
            query = query.filter(SpamHandlerData.timestamp <= end_date)

        if search:
            query = query.filter(
                or_(
                    SpamHandlerData.agent_name.ilike(f"%{search}%"),
                    SpamHandlerData.profile_name.ilike(f"%{search}%"),
                    SpamHandlerData.sender_email.ilike(f"%{search}%"),
                    SpamHandlerData.error_details.ilike(f"%{search}%"),
                )
            )

        # Order by timestamp descending (most recent first)
        query = query.order_by(desc(SpamHandlerData.timestamp))

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        items = query.offset(skip).limit(limit).all()

        return items, total

    def update(
        self, db: Session, *, db_obj: SpamHandlerData, obj_in: SpamHandlerDataUpdate
    ) -> SpamHandlerData:
        """Update a spam handler data entry"""
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[SpamHandlerData]:
        """Delete a spam handler data entry"""
        obj = db.query(SpamHandlerData).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def bulk_create(
        self, db: Session, *, objs_in: List[SpamHandlerDataCreate]
    ) -> List[SpamHandlerData]:
        """Bulk create spam handler data entries"""
        db_objs = []
        for obj_in in objs_in:
            timestamp = obj_in.timestamp or datetime.utcnow()
            db_obj = SpamHandlerData(
                agent_name=obj_in.agent_name,
                profile_name=obj_in.profile_name,
                sender_email=obj_in.sender_email,
                spam_emails_found=obj_in.spam_emails_found,
                moved_to_inbox=obj_in.moved_to_inbox,
                total_time_seconds=obj_in.total_time_seconds,
                error_occurred=obj_in.error_occurred,
                error_details=obj_in.error_details,
                timestamp=timestamp,
                spam_email_subjects=obj_in.spam_email_subjects or [],
            )
            db_objs.append(db_obj)

        if db_objs:
            db.add_all(db_objs)
            db.commit()
            for obj in db_objs:
                db.refresh(obj)

        return db_objs

    def bulk_delete(self, db: Session, *, ids: List[int]) -> int:
        """Bulk delete spam handler data entries"""
        deleted_count = (
            db.query(SpamHandlerData)
            .filter(SpamHandlerData.id.in_(ids))
            .delete(synchronize_session=False)
        )
        db.commit()
        return deleted_count

    def get_by_agent(
        self, db: Session, agent_name: str, limit: int = 100
    ) -> List[SpamHandlerData]:
        """Get spam handler data by agent name"""
        return (
            db.query(SpamHandlerData)
            .filter(SpamHandlerData.agent_name == agent_name)
            .order_by(desc(SpamHandlerData.timestamp))
            .limit(limit)
            .all()
        )

    def get_by_profile(
        self, db: Session, profile_name: str, limit: int = 100
    ) -> List[SpamHandlerData]:
        """Get spam handler data by profile name"""
        return (
            db.query(SpamHandlerData)
            .filter(SpamHandlerData.profile_name == profile_name)
            .order_by(desc(SpamHandlerData.timestamp))
            .limit(limit)
            .all()
        )

    def get_by_sender(
        self, db: Session, sender_email: str, limit: int = 100
    ) -> List[SpamHandlerData]:
        """Get spam handler data by sender email"""
        return (
            db.query(SpamHandlerData)
            .filter(SpamHandlerData.sender_email == sender_email)
            .order_by(desc(SpamHandlerData.timestamp))
            .limit(limit)
            .all()
        )

    def get_statistics(
        self,
        db: Session,
        *,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Get spam handler statistics"""
        query = db.query(SpamHandlerData)

        if start_date:
            query = query.filter(SpamHandlerData.timestamp >= start_date)
        if end_date:
            query = query.filter(SpamHandlerData.timestamp <= end_date)

        # Basic stats
        total_operations = query.count()
        if total_operations == 0:
            return {
                "total_operations": 0,
                "total_spam_found": 0,
                "total_moved_to_inbox": 0,
                "average_processing_time": 0,
                "success_rate": 0,
                "error_rate": 0,
                "top_senders": [],
                "operations_by_agent": [],
                "operations_by_profile": [],
            }

        total_spam_found = (
            query.with_entities(func.sum(SpamHandlerData.spam_emails_found)).scalar()
            or 0
        )
        total_moved_to_inbox = (
            query.with_entities(func.sum(SpamHandlerData.moved_to_inbox)).scalar() or 0
        )
        average_processing_time = (
            query.with_entities(func.avg(SpamHandlerData.total_time_seconds)).scalar()
            or 0
        )

        error_count = query.filter(SpamHandlerData.error_occurred == True).count()
        success_rate = ((total_operations - error_count) / total_operations) * 100
        error_rate = (error_count / total_operations) * 100

        # Top senders by spam found
        top_senders = (
            db.query(
                SpamHandlerData.sender_email,
                func.sum(SpamHandlerData.spam_emails_found).label("total_spam"),
                func.count(SpamHandlerData.id).label("operations"),
            )
            .group_by(SpamHandlerData.sender_email)
            .order_by(desc("total_spam"))
            .limit(10)
            .all()
        )

        # Operations by agent
        operations_by_agent = (
            db.query(
                SpamHandlerData.agent_name,
                func.count(SpamHandlerData.id).label("operations"),
                func.sum(SpamHandlerData.spam_emails_found).label("total_spam"),
            )
            .group_by(SpamHandlerData.agent_name)
            .order_by(desc("operations"))
            .all()
        )

        # Operations by profile
        operations_by_profile = (
            db.query(
                SpamHandlerData.profile_name,
                func.count(SpamHandlerData.id).label("operations"),
                func.sum(SpamHandlerData.spam_emails_found).label("total_spam"),
            )
            .group_by(SpamHandlerData.profile_name)
            .order_by(desc("operations"))
            .all()
        )

        return {
            "total_operations": total_operations,
            "total_spam_found": int(total_spam_found),
            "total_moved_to_inbox": int(total_moved_to_inbox),
            "average_processing_time": float(average_processing_time),
            "success_rate": float(success_rate),
            "error_rate": float(error_rate),
            "top_senders": [
                {
                    "sender_email": sender,
                    "total_spam": int(spam),
                    "operations": int(ops),
                }
                for sender, spam, ops in top_senders
            ],
            "operations_by_agent": [
                {"agent_name": agent, "operations": int(ops), "total_spam": int(spam)}
                for agent, ops, spam in operations_by_agent
            ],
            "operations_by_profile": [
                {
                    "profile_name": profile,
                    "operations": int(ops),
                    "total_spam": int(spam),
                }
                for profile, ops, spam in operations_by_profile
            ],
        }

    def get_recent_entries(
        self, db: Session, *, hours: int = 24, limit: int = 100
    ) -> List[SpamHandlerData]:
        """Get recent spam handler entries within specified hours"""
        since_time = datetime.utcnow() - timedelta(hours=hours)
        return (
            db.query(SpamHandlerData)
            .filter(SpamHandlerData.timestamp >= since_time)
            .order_by(desc(SpamHandlerData.timestamp))
            .limit(limit)
            .all()
        )

    def delete_old_entries(self, db: Session, *, days_old: int = 30) -> int:
        """Delete entries older than specified days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        deleted_count = (
            db.query(SpamHandlerData)
            .filter(SpamHandlerData.timestamp < cutoff_date)
            .delete(synchronize_session=False)
        )
        db.commit()
        return deleted_count


spam_handler_data = CRUDSpamHandlerData()
