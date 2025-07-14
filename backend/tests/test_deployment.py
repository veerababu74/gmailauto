#!/usr/bin/env python3
"""
Test script to verify database connection for production deployment
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.config import settings
from database import DatabaseManager
from sqlalchemy import text


def test_database_connection():
    """Test database connection with current settings"""

    print("🔍 Testing Database Connection...")
    print(f"   Database Type: {settings.DB_TYPE}")
    print(f"   Host: {settings.MYSQL_HOST}")
    print(f"   Port: {settings.MYSQL_PORT}")
    print(f"   Database: {settings.MYSQL_DATABASE}")
    print(f"   User: {settings.MYSQL_USER}")
    print("-" * 50)

    try:
        # Initialize database manager
        db_manager = DatabaseManager()

        # Test sync connection
        print("✅ Database Manager initialized successfully")

        # Test connection with a simple query
        db = next(db_manager.get_db())
        try:
            result = db.execute(text("SELECT 1 as test_value"))
            row = result.fetchone()
            print(f"✅ Database query successful: {row}")
        finally:
            db.close()

        print("✅ Database connection test passed!")
        return True

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_environment_variables():
    """Test that all required environment variables are set"""

    print("\n🔍 Testing Environment Variables...")
    print("-" * 50)

    required_vars = [
        "DB_TYPE",
        "DB_USER",
        "DB_PASS",
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "MYSQL_HOST",
        "MYSQL_PORT",
        "MYSQL_USER",
        "MYSQL_PASSWORD",
        "MYSQL_DATABASE",
        "SECRET_KEY",
    ]

    missing_vars = []

    for var in required_vars:
        value = getattr(settings, var, None)
        if not value:
            missing_vars.append(var)
            print(f"❌ Missing: {var}")
        else:
            if "PASS" in var or "SECRET" in var:
                print(f"✅ Found: {var} = ****")
            else:
                print(f"✅ Found: {var} = {value}")

    if missing_vars:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    else:
        print("\n✅ All required environment variables are set!")
        return True


def main():
    """Main test function"""

    print("🚀 Gmail Automation Backend - Database Connection Test")
    print("=" * 60)

    # Test environment variables
    env_test = test_environment_variables()

    if not env_test:
        print("\n❌ Environment variable test failed. Please check your .env file.")
        return False

    # Test database connection
    db_test = test_database_connection()

    if not db_test:
        print(
            "\n❌ Database connection test failed. Please check your database configuration."
        )
        return False

    print("\n" + "=" * 60)
    print("🎉 All tests passed! Your backend is ready for deployment.")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
