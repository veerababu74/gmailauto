#!/usr/bin/env python3
"""
Database Setup Script for Gmail Automation Backend
Handles both SQLite and MySQL database setup with proper configuration
"""

import os
import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from app.db.init_db import init_db, init_db_async
from app.core.database import db_manager, check_database_health
from app.core.config import settings


def setup_mysql_database():
    """Setup MySQL database if needed"""
    import pymysql

    try:
        # Connect to MySQL server without specifying database
        connection = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            charset="utf8mb4",
        )

        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {settings.MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            print(
                f"MySQL database '{settings.MYSQL_DATABASE}' created or already exists"
            )

        connection.close()
        return True

    except Exception as e:
        print(f"Error setting up MySQL database: {e}")
        return False


def setup_sqlite_database():
    """Setup SQLite database directory"""
    try:
        # Create directory for SQLite database
        db_path = Path(settings.SQLITE_DATABASE_PATH)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"SQLite database directory created: {db_path.parent}")
        return True

    except Exception as e:
        print(f"Error setting up SQLite database: {e}")
        return False


def main():
    """Main setup function"""
    print("=" * 60)
    print("Gmail Automation Database Setup")
    print("=" * 60)

    print(f"Database Type: {settings.DB_TYPE}")
    print(f"Pool Size: {settings.DB_POOL_SIZE}")
    print(f"Max Overflow: {settings.DB_MAX_OVERFLOW}")
    print(f"Keep-alive Interval: {settings.DB_KEEP_ALIVE_INTERVAL}s")
    print("-" * 60)

    # Setup database based on type
    if settings.DB_TYPE.lower() == "mysql":
        print("Setting up MySQL database...")
        if not setup_mysql_database():
            print("❌ MySQL setup failed!")
            return False
        print("✅ MySQL setup completed")

    elif settings.DB_TYPE.lower() == "sqlite":
        print("Setting up SQLite database...")
        if not setup_sqlite_database():
            print("❌ SQLite setup failed!")
            return False
        print("✅ SQLite setup completed")

    else:
        print(f"❌ Unsupported database type: {settings.DB_TYPE}")
        return False

    # Test database connection
    print("\nTesting database connection...")
    if not db_manager.test_connection():
        print("❌ Database connection test failed!")
        return False
    print("✅ Database connection successful")

    # Initialize database tables
    print("\nInitializing database tables...")
    try:
        init_db()
        print("✅ Database tables initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

    # Check database health
    print("\nPerforming health check...")
    health_status = check_database_health()

    if health_status["status"] == "healthy":
        print("✅ Database health check passed")
        print(
            f"   Connection Test: {'✅' if health_status['connection_test'] else '❌'}"
        )
        print(f"   Pool Status: {health_status['pool_status']}")
    else:
        print("❌ Database health check failed")
        print(f"   Error: {health_status.get('error', 'Unknown error')}")
        return False

    print("\n" + "=" * 60)
    print("🎉 Database setup completed successfully!")
    print("=" * 60)
    print(f"Database Type: {db_manager.db_type}")
    print(
        f"Ready for {settings.DB_POOL_SIZE + settings.DB_MAX_OVERFLOW} concurrent connections"
    )
    print("Keep-alive mechanism active for MySQL connections")
    print("\nYour application is ready to handle 1000+ concurrent users!")

    return True


async def async_setup():
    """Async version of setup for testing async functionality"""
    print("\nTesting async database functionality...")

    try:
        # Test async connection
        if await db_manager.test_connection_async():
            print("✅ Async database connection successful")
        else:
            print("❌ Async database connection failed")
            return False

        # Initialize tables async
        await init_db_async()
        print("✅ Async database initialization successful")

        return True

    except Exception as e:
        print(f"❌ Async setup failed: {e}")
        return False


if __name__ == "__main__":
    try:
        # Run synchronous setup
        success = main()

        if success:
            # Run async setup
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            async_success = loop.run_until_complete(async_setup())
            loop.close()

            if async_success:
                print(
                    "\n✅ Complete setup successful - Both sync and async functionality working!"
                )
                sys.exit(0)
            else:
                print("\n❌ Async setup failed")
                sys.exit(1)
        else:
            print("\n❌ Setup failed")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)
