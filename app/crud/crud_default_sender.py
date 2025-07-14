from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.default_sender import DefaultSender
from app.schemas.default_sender import DefaultSenderCreate, DefaultSenderUpdate


class CRUDDefaultSender:
    """CRUD operations for Default Sender"""

    def create(self, db: Session, *, obj_in: DefaultSenderCreate) -> DefaultSender:
        """Create a new default sender"""
        db_obj = DefaultSender(
            email=obj_in.email,
            description=obj_in.description,
            is_active=obj_in.is_active,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[DefaultSender]:
        """Get a default sender by ID"""
        return db.query(DefaultSender).filter(DefaultSender.id == id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[DefaultSender]:
        """Get a default sender by email"""
        return db.query(DefaultSender).filter(DefaultSender.email == email).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> tuple[List[DefaultSender], int]:
        """Get multiple default senders with filtering and pagination"""
        query = db.query(DefaultSender)

        # Apply filters
        if is_active is not None:
            query = query.filter(DefaultSender.is_active == is_active)

        if search:
            query = query.filter(
                or_(
                    DefaultSender.email.ilike(f"%{search}%"),
                    DefaultSender.description.ilike(f"%{search}%"),
                )
            )

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        items = query.offset(skip).limit(limit).all()

        return items, total

    def get_active(self, db: Session) -> List[DefaultSender]:
        """Get all active default senders"""
        return db.query(DefaultSender).filter(DefaultSender.is_active == True).all()

    def update(
        self, db: Session, *, db_obj: DefaultSender, obj_in: DefaultSenderUpdate
    ) -> DefaultSender:
        """Update a default sender"""
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[DefaultSender]:
        """Delete a default sender"""
        obj = db.query(DefaultSender).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def bulk_create(
        self, db: Session, *, objs_in: List[DefaultSenderCreate]
    ) -> List[DefaultSender]:
        """Bulk create default senders"""
        db_objs = []
        for obj_in in objs_in:
            # Check if email already exists
            existing = self.get_by_email(db, obj_in.email)
            if not existing:
                db_obj = DefaultSender(
                    email=obj_in.email,
                    description=obj_in.description,
                    is_active=obj_in.is_active,
                )
                db_objs.append(db_obj)

        if db_objs:
            db.add_all(db_objs)
            db.commit()
            for obj in db_objs:
                db.refresh(obj)

        return db_objs

    def bulk_delete(self, db: Session, *, ids: List[int]) -> int:
        """Bulk delete default senders"""
        deleted_count = (
            db.query(DefaultSender)
            .filter(DefaultSender.id.in_(ids))
            .delete(synchronize_session=False)
        )
        db.commit()
        return deleted_count

    def activate_all(self, db: Session) -> int:
        """Activate all default senders"""
        updated_count = db.query(DefaultSender).update({"is_active": True})
        db.commit()
        return updated_count

    def deactivate_all(self, db: Session) -> int:
        """Deactivate all default senders"""
        updated_count = db.query(DefaultSender).update({"is_active": False})
        db.commit()
        return updated_count

    def get_emails_list(self, db: Session, *, is_active: bool = True) -> List[str]:
        """Get list of email addresses only"""
        senders = (
            db.query(DefaultSender).filter(DefaultSender.is_active == is_active).all()
        )
        return [sender.email for sender in senders]


default_sender = CRUDDefaultSender()
