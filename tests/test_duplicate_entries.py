#!/usr/bin/env python3
"""
Test Duplicate Entry Handling
"""

import sys
import os
import requests
import json

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


def test_duplicate_entries():
    """Test adding duplicate entries to verify error handling"""
    base_url = "http://localhost:8000"

    # Login with test user
    login_data = {"username": "test@example.com", "password": "testpassword123"}

    print("🔐 Testing login...")
    login_response = requests.post(
        f"{base_url}/api/v1/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return

    token_data = login_response.json()
    access_token = token_data.get("access_token")
    print(f"✅ Login successful!")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Test adding a new default sender
    print("\n➕ Testing add new default sender...")
    new_sender = {
        "email": "duplicate-test@example.com",
        "description": "First attempt",
        "is_active": True,
    }

    create_response = requests.post(
        f"{base_url}/api/v1/default-senders/", headers=headers, json=new_sender
    )

    if create_response.status_code == 200:
        print(f"✅ Successfully created sender: duplicate-test@example.com")
    else:
        print(f"❌ Failed to create sender: {create_response.status_code}")
        print(f"Response: {create_response.text}")
        return

    # Test adding the same sender again (should fail)
    print("\n❌ Testing add duplicate default sender...")
    duplicate_sender = {
        "email": "duplicate-test@example.com",
        "description": "Second attempt (should fail)",
        "is_active": True,
    }

    duplicate_response = requests.post(
        f"{base_url}/api/v1/default-senders/", headers=headers, json=duplicate_sender
    )

    if duplicate_response.status_code == 400:
        error_data = duplicate_response.json()
        print(f"✅ Correctly rejected duplicate sender!")
        print(f"Error message: {error_data.get('detail', 'No error message')}")
    else:
        print(f"❌ Unexpected response: {duplicate_response.status_code}")
        print(f"Response: {duplicate_response.text}")

    # Test adding duplicate URL
    print("\n➕ Testing add new random URL...")
    new_url = {
        "url": "https://duplicate-test.com",
        "category": "other",
        "description": "First URL attempt",
        "is_active": True,
    }

    url_response = requests.post(
        f"{base_url}/api/v1/random-urls/", headers=headers, json=new_url
    )

    if url_response.status_code == 200:
        print(f"✅ Successfully created URL: https://duplicate-test.com")
    else:
        print(f"❌ Failed to create URL: {url_response.status_code}")
        print(f"Response: {url_response.text}")
        return

    # Test adding the same URL again (should fail)
    print("\n❌ Testing add duplicate random URL...")
    duplicate_url = {
        "url": "https://duplicate-test.com",
        "category": "social",
        "description": "Second URL attempt (should fail)",
        "is_active": True,
    }

    duplicate_url_response = requests.post(
        f"{base_url}/api/v1/random-urls/", headers=headers, json=duplicate_url
    )

    if duplicate_url_response.status_code == 400:
        error_data = duplicate_url_response.json()
        print(f"✅ Correctly rejected duplicate URL!")
        print(f"Error message: {error_data.get('detail', 'No error message')}")
    else:
        print(f"❌ Unexpected response: {duplicate_url_response.status_code}")
        print(f"Response: {duplicate_url_response.text}")


if __name__ == "__main__":
    test_duplicate_entries()
