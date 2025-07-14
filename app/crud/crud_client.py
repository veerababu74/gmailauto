from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate
from app.schemas.client import ClientStatus


class CRUDClient(CRUDBase[Client, ClientCreate, ClientUpdate]):
    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Client]:
        return (
            db.query(Client)
            .filter(Client.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_email(
        self, db: Session, *, email: str, user_id: int
    ) -> Optional[Client]:
        return (
            db.query(Client)
            .filter(Client.email == email, Client.user_id == user_id)
            .first()
        )

    def create_with_user(
        self, db: Session, *, obj_in: ClientCreate, user_id: int
    ) -> Client:
        obj_in_data = obj_in.dict()
        obj_in_data["user_id"] = user_id
        db_obj = Client(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_status(
        self,
        db: Session,
        *,
        user_id: int,
        status: ClientStatus,
        skip: int = 0,
        limit: int = 100
    ) -> List[Client]:
        return (
            db.query(Client)
            .filter(Client.user_id == user_id, Client.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_stats(self, db: Session, *, user_id: int) -> dict:
        total = db.query(Client).filter(Client.user_id == user_id).count()
        active = (
            db.query(Client)
            .filter(Client.user_id == user_id, Client.status == ClientStatus.ACTIVE)
            .count()
        )
        inactive = (
            db.query(Client)
            .filter(Client.user_id == user_id, Client.status == ClientStatus.INACTIVE)
            .count()
        )
        pending = (
            db.query(Client)
            .filter(Client.user_id == user_id, Client.status == ClientStatus.PENDING)
            .count()
        )
        blocked = (
            db.query(Client)
            .filter(Client.user_id == user_id, Client.status == ClientStatus.BLOCKED)
            .count()
        )

        return {
            "total_clients": total,
            "active_clients": active,
            "inactive_clients": inactive,
            "pending_clients": pending,
            "blocked_clients": blocked,
        }

    def search(
        self, db: Session, *, user_id: int, query: str, skip: int = 0, limit: int = 100
    ) -> List[Client]:
        return (
            db.query(Client)
            .filter(
                Client.user_id == user_id,
                (
                    Client.name.contains(query)
                    | Client.email.contains(query)
                    | Client.company.contains(query)
                ),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


client = CRUDClient(Client)
