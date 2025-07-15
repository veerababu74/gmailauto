"""
Database initialization using the new advanced database manager
"""

from app.core.database import db_manager, Base
from app.models import (
    user,
    client,
    campaign,
    default_sender,
    random_url,
    random_website_settings,
    connectivity_settings,
    spam_handler_data,
    email_processing_data,
    agent,
    proxy_error,
    logged_out_profile,
)  # Import all models


def init_db():
    """
    Create all database tables using the new database manager
    """
    try:
        # Test database connection first
        if not db_manager.test_connection():
            raise Exception("Database connection test failed")

        # Create all tables
        db_manager.create_tables()

        print(f"Database tables created successfully!")
        print(f"Database type: {db_manager.db_type}")
        print(f"Pool status: {db_manager.get_pool_status()}")

    except Exception as e:
        print(f"Error initializing database: {e}")
        raise


async def init_db_async():
    """
    Async version of database initialization
    """
    try:
        # Test async database connection first
        if not await db_manager.test_connection_async():
            raise Exception("Async database connection test failed")

        # Create all tables asynchronously
        await db_manager.create_tables_async()

        print(f"Database tables created successfully (async)!")
        print(f"Database type: {db_manager.db_type}")

    except Exception as e:
        print(f"Error initializing database (async): {e}")
        raise


if __name__ == "__main__":
    init_db()
