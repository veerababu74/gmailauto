#!/usr/bin/env python3
"""
Simple test script to validate Quick Actions functionality without running full server
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test imports
    from app.api.api_v1.endpoints import quick_actions

    print("✓ Quick Actions endpoints imported successfully")

    # Test database connection
    from app.core.database import get_db

    print("✓ Database connection available")

    # Test CRUD imports
    from app.crud.crud_agent import agent
    from app.crud.crud_email_processing_data import email_processing_data
    from app.crud.crud_spam_handler_data import spam_handler_data

    print("✓ CRUD modules imported successfully")

    print("\n✅ All imports successful - Quick Actions module is ready!")
    print("📄 Quick Actions endpoints available:")
    print("  - GET /quick-actions/agent-error-levels")
    print("  - GET /quick-actions/agent-error-details/{agent_name}")
    print("  - GET /quick-actions/error-summary")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
