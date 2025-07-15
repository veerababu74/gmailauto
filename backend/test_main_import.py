#!/usr/bin/env python3
"""
Test main app import
"""
try:
    from main import app

    print("✅ Main app imports successfully")
except Exception as e:
    print(f"❌ Main app import failed: {e}")
    import traceback

    traceback.print_exc()
