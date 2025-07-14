#!/usr/bin/env python3
"""
Create Test User for API Testing
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.crud_user import user
from app.schemas.user import UserCreate


def create_test_user():
    """Create a test user for API testing"""
    db_gen = get_db()
    db = next(db_gen)

    try:
        # Check if test user already exists
        existing_user = user.get_by_email(db, email="test@example.com")
        if existing_user:
            print("✅ Test user already exists: test@example.com")
            return existing_user

        # Create test user
        user_data = UserCreate(
            email="test@example.com", name="Test User", password="testpassword123"
        )

        new_user = user.create(db, obj_in=user_data)
        print(f"✅ Created test user: {new_user.email} (ID: {new_user.id})")
        return new_user

    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return None
    finally:
        db.close()


if __name__ == "__main__":
    create_test_user()
