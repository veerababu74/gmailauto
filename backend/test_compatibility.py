#!/usr/bin/env python3
"""
Test script to verify Python and package compatibility
"""
import sys

print(f"Python version: {sys.version}")

try:
    import sqlalchemy

    print(f"SQLAlchemy version: {sqlalchemy.__version__}")

    # Test the problematic import that was failing
    from sqlalchemy.sql.elements import SQLCoreOperations

    print("✓ SQLAlchemy imports successfully")

except ImportError as e:
    print(f"✗ SQLAlchemy import failed: {e}")

try:
    import pydantic

    print(f"Pydantic version: {pydantic.__version__}")

    from pydantic import BaseModel

    class TestModel(BaseModel):
        name: str

        class Config:
            orm_mode = True

    print("✓ Pydantic v1 syntax works")

except Exception as e:
    print(f"✗ Pydantic test failed: {e}")

try:
    import fastapi

    print(f"FastAPI version: {fastapi.__version__}")
    print("✓ FastAPI imports successfully")
except ImportError as e:
    print(f"✗ FastAPI import failed: {e}")

print("\nCompatibility test completed!")
