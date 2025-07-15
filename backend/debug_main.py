#!/usr/bin/env python3
"""Test script to verify main app works"""

import sys
import traceback
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

print("Testing main app import...")

try:
    from app.main import app

    print("✅ Main app imported successfully")
    print(f"App title: {app.title}")
    print(f"App version: {app.version}")
    print(f"OpenAPI URL: {app.openapi_url}")

except Exception as e:
    print(f"❌ Error importing main app: {e}")
    traceback.print_exc()
    sys.exit(1)

print("✅ Main app test completed successfully!")
