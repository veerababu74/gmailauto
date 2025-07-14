#!/usr/bin/env python3
"""
Check Users in Database
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User


def check_users():
    """Check what users exist in the database"""
    db_gen = get_db()
    db = next(db_gen)

    try:
        users = db.query(User).all()
        print(f"📧 Found {len(users)} users in database:")

        for user in users:
            print(f"   - ID: {user.id}")
            print(f"     Email: {user.email}")
            print(f"     Name: {user.name}")
            print(f"     Is Active: {user.is_active}")
            print(f"     Is Superuser: {user.is_superuser}")
            print(f"     Is Verified: {user.is_verified}")
            print(f"     Created: {user.created_at}")
            print(f"     ---")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    check_users()
