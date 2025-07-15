#!/usr/bin/env python3
"""Test script to debug main app import"""

import sys
import traceback

print("Testing FastAPI main app import...")

try:
    from app.main import app

    print("✅ FastAPI app imported successfully")
    print(f"Title: {app.title}")
    print(f"OpenAPI URL: {app.openapi_url}")
    print(f"Version: {app.version}")
except Exception as e:
    print("❌ FastAPI app import error:", e)
    traceback.print_exc()
    sys.exit(1)

print("✅ All imports successful!")
