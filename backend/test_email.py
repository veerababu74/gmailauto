#!/usr/bin/env python3
"""Test script to verify custom email validator works"""

import sys
import traceback

print("Testing custom email validator...")

try:
    from app.utils.email_validator import validate_email, EmailStr

    print("✅ Email validator imported successfully")

    # Test valid emails
    valid_emails = [
        "test@example.com",
        "user.name@domain.co.uk",
        "admin@subdomain.example.org",
    ]

    for email in valid_emails:
        try:
            result = validate_email(email)
            print(f"✅ Valid: {email} -> {result}")
        except Exception as e:
            print(f"❌ Should be valid: {email} -> {e}")

    # Test invalid emails
    invalid_emails = ["invalid-email", "@domain.com", "user@", "user@domain"]

    for email in invalid_emails:
        try:
            result = validate_email(email)
            print(f"❌ Should be invalid: {email} -> {result}")
        except Exception as e:
            print(f"✅ Correctly rejected: {email} -> {e}")

except Exception as e:
    print("❌ Email validator import error:", e)
    traceback.print_exc()
    sys.exit(1)

print("✅ Email validator tests completed!")
