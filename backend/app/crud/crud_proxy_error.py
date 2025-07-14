from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from app.models.proxy_error import ProxyError
from app.schemas.proxy_error import ProxyErrorCreate, ProxyErrorUpdate


class CRUDProxyError:
    """CRUD operations for Proxy Error"""

    def create(self, db: Session, *, obj_in: ProxyErrorCreate) -> ProxyError:
        """Create a new proxy error record"""
        db_obj = ProxyError(
            agent_name=obj_in.agent_name,
            proxy=obj_in.proxy,
            error_details=obj_in.error_details,
            profile_name=obj_in.profile_name,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[ProxyError]:
        """Get a proxy error by ID"""
        return db.query(ProxyError).filter(ProxyError.id == id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        agent_name: Optional[str] = None,
        proxy: Optional[str] = None,
        profile_name: Optional[str] = None,
        search: Optional[str] = None,
    ) -> tuple[List[ProxyError], int]:
        """Get multiple proxy errors with filtering and pagination"""
        query = db.query(ProxyError)

        # Apply filters
        if agent_name:
            query = query.filter(ProxyError.agent_name.ilike(f"%{agent_name}%"))

        if proxy:
            query = query.filter(ProxyError.proxy.ilike(f"%{proxy}%"))

        if profile_name:
            query = query.filter(ProxyError.profile_name.ilike(f"%{profile_name}%"))

        if search:
            query = query.filter(
                or_(
                    ProxyError.agent_name.ilike(f"%{search}%"),
                    ProxyError.proxy.ilike(f"%{search}%"),
                    ProxyError.profile_name.ilike(f"%{search}%"),
                    ProxyError.error_details.ilike(f"%{search}%"),
                )
            )

        # Get total count before pagination
        total = query.count()

        # Apply pagination and ordering (newest first)
        items = (
            query.order_by(desc(ProxyError.created_at)).offset(skip).limit(limit).all()
        )

        return items, total

    def update(
        self, db: Session, *, db_obj: ProxyError, obj_in: ProxyErrorUpdate
    ) -> ProxyError:
        """Update a proxy error"""
        update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ProxyError:
        """Delete a proxy error"""
        obj = db.query(ProxyError).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def get_by_agent_and_proxy(
        self, db: Session, agent_name: str, proxy: str
    ) -> List[ProxyError]:
        """Get proxy errors by agent name and proxy"""
        return (
            db.query(ProxyError)
            .filter(
                and_(
                    ProxyError.agent_name == agent_name,
                    ProxyError.proxy == proxy,
                )
            )
            .order_by(desc(ProxyError.created_at))
            .all()
        )

    def get_recent_by_agent(
        self, db: Session, agent_name: str, limit: int = 10
    ) -> List[ProxyError]:
        """Get recent proxy errors for a specific agent"""
        return (
            db.query(ProxyError)
            .filter(ProxyError.agent_name == agent_name)
            .order_by(desc(ProxyError.created_at))
            .limit(limit)
            .all()
        )

    def count_by_proxy(self, db: Session, proxy: str) -> int:
        """Count total errors for a specific proxy"""
        return db.query(ProxyError).filter(ProxyError.proxy == proxy).count()

    def get_unique_agents(self, db: Session) -> List[str]:
        """Get list of unique agent names"""
        return [
            row[0]
            for row in db.query(ProxyError.agent_name)
            .distinct()
            .order_by(ProxyError.agent_name)
            .all()
        ]

    def get_unique_proxies(self, db: Session) -> List[str]:
        """Get list of unique proxies"""
        return [
            row[0]
            for row in db.query(ProxyError.proxy)
            .distinct()
            .order_by(ProxyError.proxy)
            .all()
        ]

    def get_unique_profiles(self, db: Session) -> List[str]:
        """Get list of unique profile names"""
        return [
            row[0]
            for row in db.query(ProxyError.profile_name)
            .distinct()
            .order_by(ProxyError.profile_name)
            .all()
        ]


proxy_error = CRUDProxyError()
