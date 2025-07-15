"""
Advanced Database Configuration for Gmail Automation Backend
Supports SQLite and MySQL with connection pooling for 1000+ concurrent users
"""

import os
import logging
from typing import AsyncGenerator, Generator
from contextlib import asynccontextmanager, contextmanager
from sqlalchemy import create_engine, event, pool, text, Engine, MetaData, Connection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy.pool import QueuePool, StaticPool, NullPool
from urllib.parse import quote_plus
from app.core.config import settings
import asyncio
import time
from threading import Timer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create declarative base
Base = declarative_base()


class DatabaseManager:
    """
    Advanced Database Manager with support for SQLite and MySQL
    Handles connection pooling, keep-alive, and high concurrency
    """

    def __init__(self):
        self.engine: Engine = None
        self.async_engine: AsyncEngine = None
        self.SessionLocal: sessionmaker = None
        self.AsyncSessionLocal: async_sessionmaker = None
        self.db_type: str = None
        self.keep_alive_timer: Timer = None
        self._initialize_database()

    def _get_database_config(self) -> dict:
        """Get database configuration based on DB_TYPE environment variable"""
        db_type = settings.DB_TYPE.lower()

        if db_type == "mysql":
            return self._get_mysql_config()
        elif db_type == "sqlite":
            return self._get_sqlite_config()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    def _get_mysql_config(self) -> dict:
        """Configure MySQL database with connection pooling"""
        # Build MySQL connection URL with mysqlconnector for production
        username = quote_plus(settings.MYSQL_USER)
        password = quote_plus(settings.MYSQL_PASSWORD)
        host = settings.MYSQL_HOST
        port = settings.MYSQL_PORT
        database = settings.MYSQL_DATABASE

        # Use mysqlconnector for production (better for cloud deployments)
        sync_url = (
            f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
        )

        # Use aiomysql for async operations
        async_url = f"mysql+aiomysql://{username}:{password}@{host}:{port}/{database}"

        # Connection pool settings for high concurrency
        pool_settings = {
            "poolclass": QueuePool,
            "pool_size": settings.DB_POOL_SIZE,  # Base connections
            "max_overflow": settings.DB_MAX_OVERFLOW,  # Additional connections
            "pool_pre_ping": True,  # Validate connections before use
            "pool_recycle": settings.DB_POOL_RECYCLE,  # Recycle connections every 1 hour
            "pool_timeout": settings.DB_POOL_TIMEOUT,  # Wait time for connection
            "connect_args": {
                "charset": "utf8mb4",
                "autocommit": False,
                "connect_timeout": 60,
                "read_timeout": 30,
                "write_timeout": 30,
                "use_unicode": True,
            },
        }

        return {
            "sync_url": sync_url,
            "async_url": async_url,
            "pool_settings": pool_settings,
            "db_type": "mysql",
        }

    def _get_sqlite_config(self) -> dict:
        """Configure SQLite database"""
        database_path = settings.SQLITE_DATABASE_PATH

        # Ensure directory exists
        os.makedirs(os.path.dirname(database_path), exist_ok=True)

        sync_url = f"sqlite:///{database_path}"
        async_url = f"sqlite+aiosqlite:///{database_path}"

        # SQLite pool settings
        pool_settings = {
            "poolclass": StaticPool,
            "pool_pre_ping": True,
            "connect_args": {
                "check_same_thread": False,
                "timeout": 20,
                "isolation_level": None,
            },
        }

        return {
            "sync_url": sync_url,
            "async_url": async_url,
            "pool_settings": pool_settings,
            "db_type": "sqlite",
        }

    def _initialize_database(self):
        """Initialize database engines and sessions"""
        try:
            config = self._get_database_config()
            self.db_type = config["db_type"]

            # Create synchronous engine
            self.engine = create_engine(
                config["sync_url"], echo=settings.DB_ECHO, **config["pool_settings"]
            )

            # Create asynchronous engine (for async operations)
            if config["db_type"] == "mysql":
                self.async_engine = create_async_engine(
                    config["async_url"],
                    echo=settings.DB_ECHO,
                    pool_size=settings.DB_POOL_SIZE,
                    max_overflow=settings.DB_MAX_OVERFLOW,
                    pool_pre_ping=True,
                    pool_recycle=settings.DB_POOL_RECYCLE,
                    pool_timeout=settings.DB_POOL_TIMEOUT,
                )
            else:
                self.async_engine = create_async_engine(
                    config["async_url"], echo=settings.DB_ECHO, pool_pre_ping=True
                )

            # Create session makers
            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )

            self.AsyncSessionLocal = async_sessionmaker(
                self.async_engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
            )

            # Set up event listeners
            self._setup_event_listeners()

            # Start keep-alive mechanism
            self._start_keep_alive()

            logger.info(f"Database initialized successfully - Type: {self.db_type}")

        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def _setup_event_listeners(self):
        """Set up SQLAlchemy event listeners"""

        @event.listens_for(self.engine, "connect")
        def set_mysql_mode(dbapi_connection, connection_record):
            """Configure MySQL connection settings"""
            if self.db_type == "mysql":
                with dbapi_connection.cursor() as cursor:
                    # Set session variables for optimal performance
                    cursor.execute("SET SESSION sql_mode='STRICT_TRANS_TABLES'")
                    cursor.execute("SET SESSION autocommit=0")
                    cursor.execute("SET SESSION innodb_lock_wait_timeout=50")

        @event.listens_for(self.engine, "checkout")
        def ping_connection(dbapi_connection, connection_record, connection_proxy):
            """Ping connection on checkout to ensure it's alive"""
            connection_record.info["checkout_time"] = time.time()

        @event.listens_for(self.engine, "checkin")
        def checkin_connection(dbapi_connection, connection_record):
            """Log connection usage time"""
            if "checkout_time" in connection_record.info:
                usage_time = time.time() - connection_record.info["checkout_time"]
                if usage_time > 10:  # Log slow connections
                    logger.warning(f"Long connection usage: {usage_time:.2f}s")

    def _start_keep_alive(self):
        """Start keep-alive mechanism to prevent connection timeouts"""
        if self.db_type == "mysql":
            self._schedule_keep_alive()

    def _schedule_keep_alive(self):
        """Schedule periodic keep-alive pings"""

        def keep_alive_ping():
            try:
                with self.engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                logger.debug("Database keep-alive ping successful")
            except Exception as e:
                logger.warning(f"Keep-alive ping failed: {e}")
            finally:
                # Schedule next ping
                self.keep_alive_timer = Timer(
                    settings.DB_KEEP_ALIVE_INTERVAL, self._schedule_keep_alive
                )
                self.keep_alive_timer.daemon = True
                self.keep_alive_timer.start()

        self.keep_alive_timer = Timer(settings.DB_KEEP_ALIVE_INTERVAL, keep_alive_ping)
        self.keep_alive_timer.daemon = True
        self.keep_alive_timer.start()

    def get_db(self) -> Generator[Session, None, None]:
        """Dependency to get database session"""
        db = self.SessionLocal()
        try:
            yield db
        except Exception as e:
            db.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            db.close()

    @asynccontextmanager
    async def get_async_db(self) -> AsyncGenerator[AsyncSession, None]:
        """Async context manager to get database session"""
        async with self.AsyncSessionLocal() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Async database session error: {e}")
                raise
            finally:
                await session.close()

    async def get_async_db_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        """FastAPI dependency for async database sessions"""
        async with self.get_async_db() as session:
            yield session

    def create_tables(self):
        """Create all database tables"""
        try:
            # Use checkfirst=True to avoid attempting to recreate existing tables
            Base.metadata.create_all(bind=self.engine, checkfirst=True)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            # If it's a table already exists error, we can ignore it
            if "already exists" in str(e):
                logger.info("Some tables already exist, continuing...")
            else:
                raise

    async def create_tables_async(self):
        """Create all database tables asynchronously"""
        try:
            async with self.async_engine.begin() as conn:
                await conn.run_sync(
                    lambda sync_conn: Base.metadata.create_all(
                        sync_conn, checkfirst=True
                    )
                )
            logger.info("Database tables created successfully (async)")
        except Exception as e:
            logger.error(f"Failed to create tables (async): {e}")
            # If it's a table already exists error, we can ignore it
            if "already exists" in str(e):
                logger.info("Some tables already exist, continuing...")
            else:
                raise

    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.info("Database connection test successful")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False

    async def test_connection_async(self) -> bool:
        """Test async database connection"""
        try:
            async with self.async_engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("Async database connection test successful")
            return True
        except Exception as e:
            logger.error(f"Async database connection test failed: {e}")
            return False

    def get_pool_status(self) -> dict:
        """Get current connection pool status"""
        if hasattr(self.engine.pool, "size"):
            status = {
                "pool_size": self.engine.pool.size(),
                "checked_in": self.engine.pool.checkedin(),
                "checked_out": self.engine.pool.checkedout(),
                "overflow": self.engine.pool.overflow(),
            }
            # Only add invalidated if the method exists
            if hasattr(self.engine.pool, "invalidated"):
                status["invalidated"] = self.engine.pool.invalidated()
            return status
        return {"status": "Pool information not available"}

    def close(self):
        """Close database connections and cleanup"""
        try:
            if self.keep_alive_timer:
                self.keep_alive_timer.cancel()

            if self.engine:
                self.engine.dispose()

            # For async engine, we need to handle it properly
            if self.async_engine:
                try:
                    # Try to get current event loop
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # If loop is running, schedule disposal
                        asyncio.create_task(self.async_engine.dispose())
                    else:
                        # If no loop is running, run in new loop
                        asyncio.run(self.async_engine.dispose())
                except RuntimeError:
                    # No event loop available, skip async cleanup
                    pass

            logger.info("Database connections closed successfully")
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")

    def __del__(self):
        """Destructor to ensure cleanup"""
        self.close()


# Global database manager instance
db_manager = DatabaseManager()


# Convenience functions for backward compatibility
def get_db() -> Generator[Session, None, None]:
    """Get database session"""
    yield from db_manager.get_db()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session"""
    async with db_manager.get_async_db() as session:
        yield session


# Export commonly used objects
engine = db_manager.engine
async_engine = db_manager.async_engine
SessionLocal = db_manager.SessionLocal
AsyncSessionLocal = db_manager.AsyncSessionLocal


# Health check function
def check_database_health() -> dict:
    """Comprehensive database health check"""
    health_status = {
        "status": "healthy",
        "database_type": db_manager.db_type,
        "connection_test": False,
        "pool_status": {},
        "timestamp": time.time(),
    }

    try:
        # Test connection
        health_status["connection_test"] = db_manager.test_connection()

        # Get pool status
        health_status["pool_status"] = db_manager.get_pool_status()

        if not health_status["connection_test"]:
            health_status["status"] = "unhealthy"

    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["error"] = str(e)
        logger.error(f"Database health check failed: {e}")

    return health_status


async def check_database_health_async() -> dict:
    """Async database health check"""
    health_status = {
        "status": "healthy",
        "database_type": db_manager.db_type,
        "connection_test": False,
        "timestamp": time.time(),
    }

    try:
        health_status["connection_test"] = await db_manager.test_connection_async()

        if not health_status["connection_test"]:
            health_status["status"] = "unhealthy"

    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["error"] = str(e)
        logger.error(f"Async database health check failed: {e}")

    return health_status
