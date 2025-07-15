#!/usr/bin/env python3
"""
Test Pydantic v1 compatibility
"""
import sys

print(f"Python version: {sys.version}")

try:
    from pydantic import BaseSettings, validator, AnyHttpUrl

    print("✅ Pydantic v1 imports successful")

    class TestSettings(BaseSettings):
        test_field: str = "test"

        @validator("test_field")
        def validate_test_field(cls, v):
            return v

    settings = TestSettings()
    print("✅ Pydantic v1 validator works")

except Exception as e:
    print(f"❌ Pydantic v1 test failed: {e}")

try:
    from app.core.config import Settings

    settings = Settings()
    print("✅ Config import works")

except Exception as e:
    print(f"❌ Config import failed: {e}")

print("\n🎯 Pydantic v1 compatibility test completed!")
