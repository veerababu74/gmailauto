"""
Database Migration Script for Logged Out Profiles Table
Creates the logged_out_profiles table in the database
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.database import Base
from app.models.logged_out_profile import LoggedOutProfile
from database import DatabaseManager
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_logged_out_profiles_table():
    """Create the logged_out_profiles table"""
    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        engine = db_manager.engine

        # Create the table
        LoggedOutProfile.__table__.create(engine, checkfirst=True)
        logger.info("✅ Successfully created logged_out_profiles table")

        # Verify table creation
        with engine.connect() as connection:
            result = connection.execute(
                text(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='logged_out_profiles'"
                )
            )
            table_exists = result.fetchone() is not None

            if table_exists:
                logger.info("✅ Verified: logged_out_profiles table exists in database")
            else:
                logger.error("❌ Failed to verify table creation")

    except Exception as e:
        logger.error(f"❌ Error creating logged_out_profiles table: {str(e)}")
        raise


def insert_sample_data():
    """Insert sample data for testing (optional)"""
    try:
        from sqlalchemy.orm import sessionmaker
        from datetime import datetime

        # Initialize database manager
        db_manager = DatabaseManager()
        engine = db_manager.engine
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        # Create session
        db = SessionLocal()

        # Create sample data
        sample_data = [
            LoggedOutProfile(
                agent_name="Agent_001",
                profile_name="profile_gmail_1",
                timestamp=datetime.utcnow(),
            ),
            LoggedOutProfile(
                agent_name="Agent_002",
                profile_name="profile_gmail_2",
                timestamp=datetime.utcnow(),
            ),
        ]

        # Insert sample data
        for record in sample_data:
            db.add(record)

        db.commit()
        logger.info("✅ Successfully inserted sample logged out profile data")

        # Verify data insertion
        count = db.query(LoggedOutProfile).count()
        logger.info(f"✅ Total logged out profile records in database: {count}")

        db.close()

    except Exception as e:
        logger.error(f"❌ Error inserting sample data: {str(e)}")
        if "db" in locals():
            db.rollback()
            db.close()


if __name__ == "__main__":
    print("🚀 Creating logged_out_profiles table...")
    create_logged_out_profiles_table()

    # Ask user if they want to insert sample data
    response = input("\n📝 Do you want to insert sample data? (y/n): ").lower().strip()
    if response in ["y", "yes"]:
        print("📝 Inserting sample data...")
        insert_sample_data()

    print("\n✅ Database migration completed successfully!")
    print("\n📊 You can now use the logged out profiles API endpoints:")
    print("   - POST /api/v1/logged-out-profiles/")
    print("   - GET /api/v1/logged-out-profiles/")
    print("   - GET /api/v1/logged-out-profiles/{id}")
    print("   - PUT /api/v1/logged-out-profiles/{id}")
    print("   - DELETE /api/v1/logged-out-profiles/{id}")
    print("   - POST /gmail-automation/logged-out-profiles")
