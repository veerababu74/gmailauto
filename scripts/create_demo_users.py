import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings
from app.crud import user
from app.schemas.user import UserCreate


def create_demo_users():
    """
    Create demo users for testing
    """
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=(
            {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
        ),
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Create demo users that match the frontend demo credentials
        demo_users = [
            {"email": "admin@gmail.com", "password": "admin123", "name": "Admin User"},
            {"email": "user@gmail.com", "password": "user123", "name": "Regular User"},
            {"email": "demo@gmail.com", "password": "demo123", "name": "Demo User"},
        ]

        for user_data in demo_users:
            # Check if user already exists
            existing_user = user.get_by_email(db, email=user_data["email"])
            if not existing_user:
                user_create = UserCreate(**user_data)
                new_user = user.create(db, obj_in=user_create)
                # Mark demo users as verified automatically
                new_user.is_verified = True
                db.add(new_user)
                db.commit()
                print(f"Created user: {new_user.email}")
            else:
                # Update existing demo users to be verified
                existing_user.is_verified = True
                db.add(existing_user)
                db.commit()
                print(f"Updated user to verified: {existing_user.email}")

    except Exception as e:
        print(f"Error creating demo users: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_demo_users()
