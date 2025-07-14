"""
Database configuration using the new advanced database manager
"""

from database import (
    db_manager,
    get_db,
    get_async_db,
    Base,
    engine,
    async_engine,
    SessionLocal,
    AsyncSessionLocal,
    check_database_health,
    check_database_health_async,
)

# Re-export for backward compatibility
__all__ = [
    "db_manager",
    "get_db",
    "get_async_db",
    "Base",
    "engine",
    "async_engine",
    "SessionLocal",
    "AsyncSessionLocal",
    "check_database_health",
    "check_database_health_async",
]
