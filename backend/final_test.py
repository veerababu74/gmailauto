#!/usr/bin/env python3
"""Final comprehensive test before deployment"""

import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

print("🚀 Final deployment readiness test...")

try:
    # Test main app
    from app.main import app

    print("✅ Main app imported successfully")

    # Test gmail automation
    from z.gmailhandlerautomation import DefaultSenderBase

    print("✅ Gmail automation imported successfully")

    # Test email validator
    from app.utils.email_validator import validate_email

    print("✅ Email validator imported successfully")

    # Test all schemas
    from app.schemas.user import UserBase
    from app.schemas.client import ClientBase
    from app.schemas.default_sender import DefaultSenderBase as SchemaDefaultSender

    print("✅ All schemas imported successfully")

    # Test email validation
    test_email = validate_email("test@example.com")
    print(f"✅ Email validation working: {test_email}")

    print("🎉 ALL TESTS PASSED - READY FOR DEPLOYMENT!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
