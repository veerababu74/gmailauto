#!/usr/bin/env python3
"""Test script to debug config import issues"""

import sys
import traceback

print("Python version:", sys.version)
print("Python path:", sys.path)

try:
    import pydantic

    print("✅ Pydantic imported:", pydantic.__version__)
except ImportError as e:
    print("❌ Pydantic import error:", e)
    sys.exit(1)

try:
    import dotenv

    print("✅ python-dotenv imported")
except ImportError as e:
    print("❌ python-dotenv import error:", e)

try:
    from app.core.config import settings

    print("✅ Config imported successfully")
    print(f"Project: {settings.PROJECT_NAME}")
    print(f"Environment: {settings.ENVIRONMENT}")
except Exception as e:
    print("❌ Config import error:", e)
    traceback.print_exc()
