#!/usr/bin/env python3
"""
Test Default Sender Functionality
"""

import sys
import os
import requests
import json

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


def test_default_sender_api():
    """Test the default sender API endpoints"""
    base_url = "http://localhost:8000"

    # First, let's get a test user token
    # We'll use the test user credentials
    login_data = {"username": "test@example.com", "password": "testpassword123"}

    print("🔐 Testing login...")
    login_response = requests.post(
        f"{base_url}/api/v1/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")

        # Try with another test user
        login_data = {"username": "test@example.com", "password": "testpassword123"}

        print("🔐 Trying with alternative user...")
        login_response = requests.post(
            f"{base_url}/api/v1/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if login_response.status_code != 200:
            print(f"❌ Alternative login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return

    token_data = login_response.json()
    access_token = token_data.get("access_token")
    print(f"✅ Login successful! Token: {access_token[:20]}...")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Test getting existing default senders
    print("\n📧 Testing get default senders...")
    get_response = requests.get(f"{base_url}/api/v1/default-senders/", headers=headers)

    if get_response.status_code == 200:
        senders_data = get_response.json()
        print(f"✅ Current default senders: {len(senders_data.get('items', []))} items")
        for sender in senders_data.get("items", []):
            print(f"   - {sender['email']} (ID: {sender['id']})")
    else:
        print(f"❌ Failed to get default senders: {get_response.status_code}")
        print(f"Response: {get_response.text}")
        return

    # Test adding a new default sender
    print("\n➕ Testing add new default sender...")
    new_sender = {
        "email": "frontend-test@example.com",
        "description": "Test sender from frontend debugging",
        "is_active": True,
    }

    create_response = requests.post(
        f"{base_url}/api/v1/default-senders/", headers=headers, json=new_sender
    )

    if create_response.status_code == 200:
        created_sender = create_response.json()
        print(
            f"✅ Successfully created sender: {created_sender['email']} (ID: {created_sender['id']})"
        )
    else:
        print(f"❌ Failed to create sender: {create_response.status_code}")
        print(f"Response: {create_response.text}")
        return

    # Test getting senders again to confirm it was added
    print("\n📧 Testing get default senders after creation...")
    get_response2 = requests.get(f"{base_url}/api/v1/default-senders/", headers=headers)

    if get_response2.status_code == 200:
        senders_data2 = get_response2.json()
        print(
            f"✅ Default senders after creation: {len(senders_data2.get('items', []))} items"
        )
        for sender in senders_data2.get("items", []):
            print(f"   - {sender['email']} (ID: {sender['id']})")
    else:
        print(
            f"❌ Failed to get default senders after creation: {get_response2.status_code}"
        )
        print(f"Response: {get_response2.text}")


if __name__ == "__main__":
    test_default_sender_api()
