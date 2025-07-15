#!/usr/bin/env python3
"""Test script to verify client schema works with custom email validator"""

import sys
import traceback

print("Testing client schema with custom email validator...")

try:
    from app.schemas.client import ClientBase, ClientCreate, ClientUpdate, ClientInDB

    print("✅ Client schemas imported successfully")

    # Test creating a client with valid email
    client_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "company": "Example Corp",
        "phone": "+1234567890",
    }

    client = ClientCreate(**client_data)
    print(f"✅ Valid client created: {client.name} - {client.email}")

    # Test client update with valid email
    update_data = {"email": "john.updated@example.com"}

    client_update = ClientUpdate(**update_data)
    print(f"✅ Valid client update: {client_update.email}")

    # Test invalid email (should raise error)
    try:
        invalid_client = ClientCreate(name="Test", email="invalid-email")
        print(f"❌ Should have failed with invalid email: {invalid_client.email}")
    except Exception as e:
        print(f"✅ Correctly rejected invalid email: {e}")

except Exception as e:
    print("❌ Client schema test error:", e)
    traceback.print_exc()
    sys.exit(1)

print("✅ Client schema tests completed!")
