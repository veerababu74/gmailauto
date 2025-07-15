#!/usr/bin/env python3

"""
Test script to verify that all database models can be created successfully with MySQL.
This script will help identify any remaining VARCHAR length issues.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.database import Base

# Import all models to ensure they're registered
from app.models import *

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_mysql_models():
    """Test that all models can be created in MySQL"""

    # Use environment variables for database connection
    DB_USER = os.getenv("DB_USER", "fundsill_babu")
    DB_PASS = os.getenv("DB_PASS", "Babu@7474")
    DB_HOST = os.getenv("DB_HOST", "45.113.224.7")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "fundsill_gmail_automation")

    # Create connection URL
    DATABASE_URL = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    try:
        # Create engine
        engine = create_engine(DATABASE_URL)

        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("✅ Database connection successful")

        # Test table creation
        logger.info("🔨 Creating tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ All tables created successfully!")

        # List all tables that were created
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            logger.info(f"📋 Created tables: {', '.join(tables)}")

        logger.info("🎉 All models are MySQL-compatible!")
        return True

    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = test_mysql_models()
    sys.exit(0 if success else 1)
