#!/usr/bin/env python3
"""Test script to debug import issues"""

import sys
import traceback
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

print("Testing step by step imports...")

try:
    print("1. Testing app.utils.email_validator...")
    from app.utils.email_validator import EmailStr, validate_email

    print("✅ Email validator imported successfully")

    print("2. Testing pydantic imports...")
    from pydantic import BaseModel, validator

    print("✅ Pydantic imports successful")

    print("3. Testing z.gmailhandlerautomation import...")
    from z.gmailhandlerautomation import DefaultSenderBase

    print("✅ Gmail handler automation imported successfully")

    print("4. Testing DefaultSenderBase creation...")
    sender = DefaultSenderBase(
        email="test@example.com", description="Test sender", is_active=True
    )
    print(f"✅ DefaultSenderBase created: {sender.email}")

except Exception as e:
    print(f"❌ Error during import: {e}")
    traceback.print_exc()
    sys.exit(1)

print("✅ All tests completed successfully!")
