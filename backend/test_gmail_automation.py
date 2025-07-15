#!/usr/bin/env python3
"""Test script to verify gmailhandlerautomation works with custom email validator"""

import sys
import traceback

print("Testing gmailhandlerautomation with custom email validator...")

try:
    from z.gmailhandlerautomation import (
        DefaultSenderBase,
        DefaultSenderCreate,
        DefaultSenderUpdate,
        SpamHandlerDataCreate,
        EmailProcessingDataCreate,
    )

    print("✅ All schemas imported successfully")

    # Test DefaultSenderBase
    sender_data = {
        "email": "test@example.com",
        "description": "Test sender",
        "is_active": True,
    }

    sender = DefaultSenderBase(**sender_data)
    print(f"✅ DefaultSenderBase created: {sender.email}")

    # Test DefaultSenderUpdate
    update_data = {"email": "updated@example.com"}

    sender_update = DefaultSenderUpdate(**update_data)
    print(f"✅ DefaultSenderUpdate created: {sender_update.email}")

    # Test SpamHandlerDataCreate
    spam_data = {
        "agent_name": "test_agent",
        "profile_name": "test_profile",
        "sender_email": "spam@example.com",
        "spam_emails_found": 5,
    }

    spam_handler = SpamHandlerDataCreate(**spam_data)
    print(f"✅ SpamHandlerDataCreate created: {spam_handler.sender_email}")

    # Test EmailProcessingDataCreate
    email_data = {
        "agent_name": "test_agent",
        "profile_name": "test_profile",
        "sender_email": "processing@example.com",
        "email_subject": "Test Subject",
    }

    email_processing = EmailProcessingDataCreate(**email_data)
    print(f"✅ EmailProcessingDataCreate created: {email_processing.sender_email}")

    # Test invalid email (should raise error)
    try:
        invalid_sender = DefaultSenderBase(email="invalid-email", description="Test")
        print(f"❌ Should have failed with invalid email: {invalid_sender.email}")
    except Exception as e:
        print(f"✅ Correctly rejected invalid email: {e}")

except Exception as e:
    print("❌ Gmail handler automation test error:", e)
    traceback.print_exc()
    sys.exit(1)

print("✅ Gmail handler automation tests completed!")
