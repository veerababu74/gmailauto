#!/usr/bin/env python3
"""
Test script to verify database initialization works correctly
"""
import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.database import db_manager
from app.models import *  # Import all models


def test_database_initialization():
    """Test database initialization"""
    print("Testing database initialization...")

    try:
        # Test database connection
        print("Testing database connection...")
        if db_manager.test_connection():
            print("✅ Database connection successful")
        else:
            print("❌ Database connection failed")
            return False

        # Test table creation
        print("Testing table creation...")
        db_manager.create_tables()
        print("✅ Table creation successful")

        # Test pool status
        print("Testing pool status...")
        try:
            pool_status = db_manager.get_pool_status()
            print(f"✅ Pool status: {pool_status}")
        except Exception as pool_error:
            print(f"⚠️  Pool status check failed (non-critical): {pool_error}")

        return True

    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False


if __name__ == "__main__":
    success = test_database_initialization()
    if success:
        print("\n🎉 All database tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Database tests failed!")
        sys.exit(1)
