from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.core.email import generate_verification_token, get_token_expiry


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            name=obj_in.name,
            hashed_password=get_password_hash(obj_in.password),
            phone=obj_in.phone,
            company=obj_in.company,
            bio=obj_in.bio,
            avatar_url=obj_in.avatar_url,
            is_active=obj_in.is_active,
            email_notifications=obj_in.email_notifications,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def update_gmail_tokens(
        self, db: Session, *, user: User, token: str, refresh_token: str
    ) -> User:
        user.gmail_token = token
        user.gmail_refresh_token = refresh_token
        user.gmail_connected = True
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def disconnect_gmail(self, db: Session, *, user: User) -> User:
        user.gmail_token = None
        user.gmail_refresh_token = None
        user.gmail_connected = False
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def is_verified(self, user: User) -> bool:
        """Check if user is verified"""
        return user.is_verified

    def create_verification_token(self, db: Session, *, user: User) -> str:
        """Create verification token for user"""
        token = generate_verification_token()
        user.verification_token = token
        user.verification_token_expires = get_token_expiry(24)  # 24 hours
        db.add(user)
        db.commit()
        db.refresh(user)
        return token

    def verify_email(self, db: Session, *, token: str) -> Optional[User]:
        """Verify user email with token"""
        user = (
            db.query(User)
            .filter(
                User.verification_token == token,
                User.verification_token_expires > datetime.utcnow(),
            )
            .first()
        )

        if user:
            user.is_verified = True
            user.verification_token = None
            user.verification_token_expires = None
            db.add(user)
            db.commit()
            db.refresh(user)

        return user

    def create_password_reset_token(self, db: Session, *, user: User) -> str:
        """Create password reset token for user"""
        token = generate_verification_token()
        user.reset_password_token = token
        user.reset_password_token_expires = get_token_expiry(1)  # 1 hour
        db.add(user)
        db.commit()
        db.refresh(user)
        return token

    def reset_password(
        self, db: Session, *, token: str, new_password: str
    ) -> Optional[User]:
        """Reset user password with token"""
        user = (
            db.query(User)
            .filter(
                User.reset_password_token == token,
                User.reset_password_token_expires > datetime.utcnow(),
            )
            .first()
        )

        if user:
            user.hashed_password = get_password_hash(new_password)
            user.reset_password_token = None
            user.reset_password_token_expires = None
            db.add(user)
            db.commit()
            db.refresh(user)

        return user

    def get_by_verification_token(self, db: Session, *, token: str) -> Optional[User]:
        """Get user by verification token"""
        return (
            db.query(User)
            .filter(
                User.verification_token == token,
                User.verification_token_expires > datetime.utcnow(),
            )
            .first()
        )

    def get_by_reset_token(self, db: Session, *, token: str) -> Optional[User]:
        """Get user by password reset token"""
        return (
            db.query(User)
            .filter(
                User.reset_password_token == token,
                User.reset_password_token_expires > datetime.utcnow(),
            )
            .first()
        )


user = CRUDUser(User)
