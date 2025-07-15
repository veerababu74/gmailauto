#!/usr/bin/env python3
"""
Test script to verify FastAPI app startup with database initialization
"""
import os
import sys
from pathlib import Path
import asyncio

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.db.init_db import init_db
from main import app


async def test_fastapi_startup():
    """Test FastAPI startup with database initialization"""
    print("Testing FastAPI startup with database initialization...")

    try:
        # Test database initialization directly
        print("1. Testing database initialization...")
        init_db()
        print("✅ Database initialization successful")

        # Test FastAPI app creation
        print("2. Testing FastAPI app creation...")
        print(f"✅ FastAPI app created: {app.title}")

        # Test app routes
        print("3. Testing app routes...")
        routes = [route.path for route in app.routes]
        print(f"✅ Found {len(routes)} routes")

        return True

    except Exception as e:
        print(f"❌ FastAPI startup failed: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_fastapi_startup())
    if success:
        print("\n🎉 FastAPI startup test passed!")
        sys.exit(0)
    else:
        print("\n💥 FastAPI startup test failed!")
        sys.exit(1)
