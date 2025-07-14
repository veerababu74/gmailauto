from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from datetime import datetime, timedelta

from app.models.email_processing_data import EmailProcessingData
from app.schemas.email_processing_data import (
    EmailProcessingDataCreate,
    EmailProcessingDataUpdate,
)


class CRUDEmailProcessingData:
    """CRUD operations for Email Processing Data"""

    def create(
        self, db: Session, *, obj_in: EmailProcessingDataCreate
    ) -> EmailProcessingData:
        """Create a new email processing data entry"""
        # Set timestamp if not provided
        timestamp = obj_in.timestamp or datetime.utcnow()

        db_obj = EmailProcessingData(
            agent_name=obj_in.agent_name,
            profile_name=obj_in.profile_name,
            sender_email=obj_in.sender_email,
            email_subject=obj_in.email_subject,
            is_opened=obj_in.is_opened,
            is_link_clicked=obj_in.is_link_clicked,
            is_unsubscribe_clicked=obj_in.is_unsubscribe_clicked,
            is_reply_sent=obj_in.is_reply_sent,
            random_website_visited=obj_in.random_website_visited,
            random_website_duration_seconds=obj_in.random_website_duration_seconds,
            total_duration_seconds=obj_in.total_duration_seconds,
            error_occurred=obj_in.error_occurred,
            error_details=obj_in.error_details,
            timestamp=timestamp,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[EmailProcessingData]:
        """Get an email processing data entry by ID"""
        return (
            db.query(EmailProcessingData).filter(EmailProcessingData.id == id).first()
        )

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        agent_name: Optional[str] = None,
        profile_name: Optional[str] = None,
        sender_email: Optional[str] = None,
        is_opened: Optional[bool] = None,
        is_link_clicked: Optional[bool] = None,
        is_unsubscribe_clicked: Optional[bool] = None,
        is_reply_sent: Optional[bool] = None,
        error_occurred: Optional[bool] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        search: Optional[str] = None,
    ) -> tuple[List[EmailProcessingData], int]:
        """Get multiple email processing data entries with filtering and pagination"""
        query = db.query(EmailProcessingData)

        # Apply filters
        if agent_name:
            query = query.filter(
                EmailProcessingData.agent_name.ilike(f"%{agent_name}%")
            )

        if profile_name:
            query = query.filter(
                EmailProcessingData.profile_name.ilike(f"%{profile_name}%")
            )

        if sender_email:
            query = query.filter(
                EmailProcessingData.sender_email.ilike(f"%{sender_email}%")
            )

        if is_opened is not None:
            query = query.filter(EmailProcessingData.is_opened == is_opened)

        if is_link_clicked is not None:
            query = query.filter(EmailProcessingData.is_link_clicked == is_link_clicked)

        if is_unsubscribe_clicked is not None:
            query = query.filter(
                EmailProcessingData.is_unsubscribe_clicked == is_unsubscribe_clicked
            )

        if is_reply_sent is not None:
            query = query.filter(EmailProcessingData.is_reply_sent == is_reply_sent)

        if error_occurred is not None:
            query = query.filter(EmailProcessingData.error_occurred == error_occurred)

        if start_date:
            query = query.filter(EmailProcessingData.timestamp >= start_date)

        if end_date:
            query = query.filter(EmailProcessingData.timestamp <= end_date)

        if search:
            query = query.filter(
                or_(
                    EmailProcessingData.agent_name.ilike(f"%{search}%"),
                    EmailProcessingData.profile_name.ilike(f"%{search}%"),
                    EmailProcessingData.sender_email.ilike(f"%{search}%"),
                    EmailProcessingData.email_subject.ilike(f"%{search}%"),
                    EmailProcessingData.random_website_visited.ilike(f"%{search}%"),
                    EmailProcessingData.error_details.ilike(f"%{search}%"),
                )
            )

        # Order by timestamp descending (most recent first)
        query = query.order_by(desc(EmailProcessingData.timestamp))

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        items = query.offset(skip).limit(limit).all()

        return items, total

    def update(
        self,
        db: Session,
        *,
        db_obj: EmailProcessingData,
        obj_in: EmailProcessingDataUpdate,
    ) -> EmailProcessingData:
        """Update an email processing data entry"""
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[EmailProcessingData]:
        """Delete an email processing data entry"""
        obj = db.query(EmailProcessingData).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def bulk_create(
        self, db: Session, *, objs_in: List[EmailProcessingDataCreate]
    ) -> List[EmailProcessingData]:
        """Bulk create email processing data entries"""
        db_objs = []
        for obj_in in objs_in:
            timestamp = obj_in.timestamp or datetime.utcnow()
            db_obj = EmailProcessingData(
                agent_name=obj_in.agent_name,
                profile_name=obj_in.profile_name,
                sender_email=obj_in.sender_email,
                email_subject=obj_in.email_subject,
                is_opened=obj_in.is_opened,
                is_link_clicked=obj_in.is_link_clicked,
                is_unsubscribe_clicked=obj_in.is_unsubscribe_clicked,
                is_reply_sent=obj_in.is_reply_sent,
                random_website_visited=obj_in.random_website_visited,
                random_website_duration_seconds=obj_in.random_website_duration_seconds,
                total_duration_seconds=obj_in.total_duration_seconds,
                error_occurred=obj_in.error_occurred,
                error_details=obj_in.error_details,
                timestamp=timestamp,
            )
            db_objs.append(db_obj)

        if db_objs:
            db.add_all(db_objs)
            db.commit()
            for obj in db_objs:
                db.refresh(obj)

        return db_objs

    def bulk_delete(self, db: Session, *, ids: List[int]) -> int:
        """Bulk delete email processing data entries"""
        deleted_count = (
            db.query(EmailProcessingData)
            .filter(EmailProcessingData.id.in_(ids))
            .delete(synchronize_session=False)
        )
        db.commit()
        return deleted_count

    def get_by_agent(
        self, db: Session, agent_name: str, limit: int = 100
    ) -> List[EmailProcessingData]:
        """Get email processing data by agent name"""
        return (
            db.query(EmailProcessingData)
            .filter(EmailProcessingData.agent_name == agent_name)
            .order_by(desc(EmailProcessingData.timestamp))
            .limit(limit)
            .all()
        )

    def get_by_profile(
        self, db: Session, profile_name: str, limit: int = 100
    ) -> List[EmailProcessingData]:
        """Get email processing data by profile name"""
        return (
            db.query(EmailProcessingData)
            .filter(EmailProcessingData.profile_name == profile_name)
            .order_by(desc(EmailProcessingData.timestamp))
            .limit(limit)
            .all()
        )

    def get_by_sender(
        self, db: Session, sender_email: str, limit: int = 100
    ) -> List[EmailProcessingData]:
        """Get email processing data by sender email"""
        return (
            db.query(EmailProcessingData)
            .filter(EmailProcessingData.sender_email == sender_email)
            .order_by(desc(EmailProcessingData.timestamp))
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
        """Get email processing statistics"""
        query = db.query(EmailProcessingData)

        if start_date:
            query = query.filter(EmailProcessingData.timestamp >= start_date)
        if end_date:
            query = query.filter(EmailProcessingData.timestamp <= end_date)

        # Basic stats
        total_emails_processed = query.count()
        if total_emails_processed == 0:
            return {
                "total_emails_processed": 0,
                "emails_opened": 0,
                "links_clicked": 0,
                "unsubscribe_clicked": 0,
                "replies_sent": 0,
                "average_processing_time": 0,
                "average_website_duration": 0,
                "success_rate": 0,
                "error_rate": 0,
                "top_senders": [],
                "processing_by_agent": [],
                "processing_by_profile": [],
                "website_visit_stats": [],
            }

        emails_opened = query.filter(EmailProcessingData.is_opened == True).count()
        links_clicked = query.filter(
            EmailProcessingData.is_link_clicked == True
        ).count()
        unsubscribe_clicked = query.filter(
            EmailProcessingData.is_unsubscribe_clicked == True
        ).count()
        replies_sent = query.filter(EmailProcessingData.is_reply_sent == True).count()

        average_processing_time = (
            query.with_entities(
                func.avg(EmailProcessingData.total_duration_seconds)
            ).scalar()
            or 0
        )
        average_website_duration = (
            query.with_entities(
                func.avg(EmailProcessingData.random_website_duration_seconds)
            ).scalar()
            or 0
        )

        error_count = query.filter(EmailProcessingData.error_occurred == True).count()
        success_rate = (
            (total_emails_processed - error_count) / total_emails_processed
        ) * 100
        error_rate = (error_count / total_emails_processed) * 100

        # Top senders by email count
        top_senders = (
            db.query(
                EmailProcessingData.sender_email,
                func.count(EmailProcessingData.id).label("email_count"),
                func.avg(EmailProcessingData.total_duration_seconds).label("avg_time"),
            )
            .group_by(EmailProcessingData.sender_email)
            .order_by(desc("email_count"))
            .limit(10)
            .all()
        )

        # Processing by agent
        processing_by_agent = (
            db.query(
                EmailProcessingData.agent_name,
                func.count(EmailProcessingData.id).label("emails_processed"),
                func.avg(EmailProcessingData.total_duration_seconds).label("avg_time"),
            )
            .group_by(EmailProcessingData.agent_name)
            .order_by(desc("emails_processed"))
            .all()
        )

        # Processing by profile
        processing_by_profile = (
            db.query(
                EmailProcessingData.profile_name,
                func.count(EmailProcessingData.id).label("emails_processed"),
                func.avg(EmailProcessingData.total_duration_seconds).label("avg_time"),
            )
            .group_by(EmailProcessingData.profile_name)
            .order_by(desc("emails_processed"))
            .all()
        )

        # Website visit stats
        website_visit_stats = (
            db.query(
                EmailProcessingData.random_website_visited,
                func.count(EmailProcessingData.id).label("visit_count"),
                func.avg(EmailProcessingData.random_website_duration_seconds).label(
                    "avg_duration"
                ),
            )
            .filter(EmailProcessingData.random_website_visited.isnot(None))
            .group_by(EmailProcessingData.random_website_visited)
            .order_by(desc("visit_count"))
            .limit(10)
            .all()
        )

        return {
            "total_emails_processed": total_emails_processed,
            "emails_opened": emails_opened,
            "links_clicked": links_clicked,
            "unsubscribe_clicked": unsubscribe_clicked,
            "replies_sent": replies_sent,
            "average_processing_time": float(average_processing_time),
            "average_website_duration": float(average_website_duration),
            "success_rate": float(success_rate),
            "error_rate": float(error_rate),
            "top_senders": [
                {
                    "sender_email": sender,
                    "email_count": int(count),
                    "avg_time": float(avg_time),
                }
                for sender, count, avg_time in top_senders
            ],
            "processing_by_agent": [
                {
                    "agent_name": agent,
                    "emails_processed": int(count),
                    "avg_time": float(avg_time),
                }
                for agent, count, avg_time in processing_by_agent
            ],
            "processing_by_profile": [
                {
                    "profile_name": profile,
                    "emails_processed": int(count),
                    "avg_time": float(avg_time),
                }
                for profile, count, avg_time in processing_by_profile
            ],
            "website_visit_stats": [
                {
                    "website": website,
                    "visit_count": int(count),
                    "avg_duration": float(duration),
                }
                for website, count, duration in website_visit_stats
                if website
            ],
        }

    def get_analytics(
        self,
        db: Session,
        *,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, float]:
        """Get email processing analytics with rates"""
        query = db.query(EmailProcessingData)

        if start_date:
            query = query.filter(EmailProcessingData.timestamp >= start_date)
        if end_date:
            query = query.filter(EmailProcessingData.timestamp <= end_date)

        total_processed = query.count()
        if total_processed == 0:
            return {
                "open_rate": 0.0,
                "click_rate": 0.0,
                "unsubscribe_rate": 0.0,
                "reply_rate": 0.0,
                "error_rate": 0.0,
                "avg_processing_time": 0.0,
                "avg_website_time": 0.0,
                "total_processed": 0,
            }

        opened = query.filter(EmailProcessingData.is_opened == True).count()
        clicked = query.filter(EmailProcessingData.is_link_clicked == True).count()
        unsubscribed = query.filter(
            EmailProcessingData.is_unsubscribe_clicked == True
        ).count()
        replied = query.filter(EmailProcessingData.is_reply_sent == True).count()
        errors = query.filter(EmailProcessingData.error_occurred == True).count()

        avg_processing_time = (
            query.with_entities(
                func.avg(EmailProcessingData.total_duration_seconds)
            ).scalar()
            or 0
        )
        avg_website_time = (
            query.with_entities(
                func.avg(EmailProcessingData.random_website_duration_seconds)
            ).scalar()
            or 0
        )

        return {
            "open_rate": (opened / total_processed) * 100,
            "click_rate": (clicked / total_processed) * 100,
            "unsubscribe_rate": (unsubscribed / total_processed) * 100,
            "reply_rate": (replied / total_processed) * 100,
            "error_rate": (errors / total_processed) * 100,
            "avg_processing_time": float(avg_processing_time),
            "avg_website_time": float(avg_website_time),
            "total_processed": total_processed,
        }

    def get_recent_entries(
        self, db: Session, *, hours: int = 24, limit: int = 100
    ) -> List[EmailProcessingData]:
        """Get recent email processing entries within specified hours"""
        since_time = datetime.utcnow() - timedelta(hours=hours)
        return (
            db.query(EmailProcessingData)
            .filter(EmailProcessingData.timestamp >= since_time)
            .order_by(desc(EmailProcessingData.timestamp))
            .limit(limit)
            .all()
        )

    def delete_old_entries(self, db: Session, *, days_old: int = 30) -> int:
        """Delete entries older than specified days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        deleted_count = (
            db.query(EmailProcessingData)
            .filter(EmailProcessingData.timestamp < cutoff_date)
            .delete(synchronize_session=False)
        )
        db.commit()
        return deleted_count


email_processing_data = CRUDEmailProcessingData()
