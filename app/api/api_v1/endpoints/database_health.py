"""
Database health check endpoint
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.core.database import (
    check_database_health,
    check_database_health_async,
    db_manager,
)

router = APIRouter()


@router.get("/health", response_model=Dict[str, Any])
async def database_health_check():
    """
    Check database health and connection status
    """
    try:
        health_status = await check_database_health_async()

        if health_status["status"] == "unhealthy":
            raise HTTPException(
                status_code=503,
                detail=f"Database is unhealthy: {health_status.get('error', 'Unknown error')}",
            )

        return health_status
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@router.get("/pool-status", response_model=Dict[str, Any])
def get_pool_status():
    """
    Get current database connection pool status
    """
    try:
        pool_status = db_manager.get_pool_status()
        return {
            "database_type": db_manager.db_type,
            "pool_status": pool_status,
            "status": "active",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get pool status: {str(e)}"
        )


@router.post("/test-connection")
async def test_database_connection():
    """
    Test database connection manually
    """
    try:
        sync_test = db_manager.test_connection()
        async_test = await db_manager.test_connection_async()

        return {
            "sync_connection": sync_test,
            "async_connection": async_test,
            "database_type": db_manager.db_type,
            "overall_status": "healthy" if sync_test and async_test else "unhealthy",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection test failed: {str(e)}")
