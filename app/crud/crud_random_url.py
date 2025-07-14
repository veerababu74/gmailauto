from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.random_url import RandomUrl
from app.schemas.random_url import RandomUrlCreate, RandomUrlUpdate


class CRUDRandomUrl:
    """CRUD operations for Random URL"""

    def create(self, db: Session, *, obj_in: RandomUrlCreate) -> RandomUrl:
        """Create a new random URL"""
        db_obj = RandomUrl(
            url=str(obj_in.url),
            description=obj_in.description,
            category=obj_in.category,
            is_active=obj_in.is_active,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[RandomUrl]:
        """Get a random URL by ID"""
        return db.query(RandomUrl).filter(RandomUrl.id == id).first()

    def get_by_url(self, db: Session, url: str) -> Optional[RandomUrl]:
        """Get a random URL by URL"""
        return db.query(RandomUrl).filter(RandomUrl.url == url).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        category: Optional[str] = None,
        search: Optional[str] = None,
    ) -> tuple[List[RandomUrl], int]:
        """Get multiple random URLs with filtering and pagination"""
        query = db.query(RandomUrl)

        # Apply filters
        if is_active is not None:
            query = query.filter(RandomUrl.is_active == is_active)

        if category:
            query = query.filter(RandomUrl.category == category.lower())

        if search:
            query = query.filter(
                or_(
                    RandomUrl.url.ilike(f"%{search}%"),
                    RandomUrl.description.ilike(f"%{search}%"),
                    RandomUrl.category.ilike(f"%{search}%"),
                )
            )

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        items = query.offset(skip).limit(limit).all()

        return items, total

    def get_active(self, db: Session) -> List[RandomUrl]:
        """Get all active random URLs"""
        return db.query(RandomUrl).filter(RandomUrl.is_active == True).all()

    def get_by_category(self, db: Session, category: str) -> List[RandomUrl]:
        """Get all URLs by category"""
        return (
            db.query(RandomUrl)
            .filter(
                and_(
                    RandomUrl.category == category.lower(), RandomUrl.is_active == True
                )
            )
            .all()
        )

    def get_categories(self, db: Session) -> List[str]:
        """Get all unique categories"""
        categories = (
            db.query(RandomUrl.category)
            .filter(RandomUrl.category.isnot(None))
            .distinct()
            .all()
        )
        return [cat[0] for cat in categories if cat[0]]

    def update(
        self, db: Session, *, db_obj: RandomUrl, obj_in: RandomUrlUpdate
    ) -> RandomUrl:
        """Update a random URL"""
        update_data = obj_in.dict(exclude_unset=True)
        if "url" in update_data:
            update_data["url"] = str(update_data["url"])

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[RandomUrl]:
        """Delete a random URL"""
        obj = db.query(RandomUrl).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def bulk_create(
        self, db: Session, *, objs_in: List[RandomUrlCreate]
    ) -> List[RandomUrl]:
        """Bulk create random URLs"""
        db_objs = []
        for obj_in in objs_in:
            # Check if URL already exists
            existing = self.get_by_url(db, str(obj_in.url))
            if not existing:
                db_obj = RandomUrl(
                    url=str(obj_in.url),
                    description=obj_in.description,
                    category=obj_in.category,
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
        """Bulk delete random URLs"""
        deleted_count = (
            db.query(RandomUrl)
            .filter(RandomUrl.id.in_(ids))
            .delete(synchronize_session=False)
        )
        db.commit()
        return deleted_count

    def activate_all(self, db: Session) -> int:
        """Activate all random URLs"""
        updated_count = db.query(RandomUrl).update({"is_active": True})
        db.commit()
        return updated_count

    def deactivate_all(self, db: Session) -> int:
        """Deactivate all random URLs"""
        updated_count = db.query(RandomUrl).update({"is_active": False})
        db.commit()
        return updated_count

    def get_urls_list(
        self, db: Session, *, is_active: bool = True, category: Optional[str] = None
    ) -> List[str]:
        """Get list of URLs only"""
        query = db.query(RandomUrl).filter(RandomUrl.is_active == is_active)
        if category:
            query = query.filter(RandomUrl.category == category.lower())

        urls = query.all()
        return [url.url for url in urls]

    def get_random_urls(
        self, db: Session, *, limit: int = 10, category: Optional[str] = None
    ) -> List[RandomUrl]:
        """Get random URLs (shuffled)"""
        from sqlalchemy import func

        query = db.query(RandomUrl).filter(RandomUrl.is_active == True)
        if category:
            query = query.filter(RandomUrl.category == category.lower())

        # Use database random function (for SQLite use RANDOM())
        return query.order_by(func.random()).limit(limit).all()


random_url = CRUDRandomUrl()
