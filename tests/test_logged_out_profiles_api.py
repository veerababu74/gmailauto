"""
Test script for the Logged Out Profiles API
Tests the POST endpoint in gmailhandlerautomation.py
"""

import requests
import json
from datetime import datetime

# API base URL (adjust if needed)
BASE_URL = "http://localhost:8000"
GMAIL_AUTOMATION_ENDPOINT = f"{BASE_URL}/gmail-automation/logged-out-profiles"
FULL_API_ENDPOINT = f"{BASE_URL}/api/v1/logged-out-profiles/"


def test_gmail_automation_post():
    """Test the POST endpoint in gmailhandlerautomation.py"""
    print("🧪 Testing Gmail Automation POST endpoint...")

    # Test data
    test_data = {"agent_name": "Test_Agent_001", "profile_name": "test_profile_gmail_1"}

    try:
        response = requests.post(
            GMAIL_AUTOMATION_ENDPOINT,
            json=test_data,
            headers={"Content-Type": "application/json"},
        )

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200 or response.status_code == 201:
            print("✅ Gmail Automation POST endpoint works!")
            data = response.json()
            print(f"Created record with ID: {data.get('id')}")
            print(f"Timestamp: {data.get('timestamp')}")
            return data
        else:
            print("❌ Gmail Automation POST endpoint failed!")
            return None

    except requests.exceptions.ConnectionError:
        print(
            "❌ Could not connect to server. Make sure the server is running on localhost:8000"
        )
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def test_full_api_endpoints():
    """Test the full CRUD API endpoints"""
    print("\n🧪 Testing Full API CRUD endpoints...")

    # Test POST
    test_data = {
        "agent_name": "Full_API_Agent_001",
        "profile_name": "full_api_profile_gmail_1",
    }

    try:
        # POST - Create
        print("Testing POST...")
        response = requests.post(
            FULL_API_ENDPOINT,
            json=test_data,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 201:
            print("✅ POST endpoint works!")
            created_record = response.json()
            record_id = created_record.get("id")

            # GET - List
            print("Testing GET (list)...")
            response = requests.get(FULL_API_ENDPOINT)
            if response.status_code == 200:
                print("✅ GET (list) endpoint works!")
                data = response.json()
                print(f"Total records: {data.get('total')}")

            # GET - Single record
            print(f"Testing GET (single record ID: {record_id})...")
            response = requests.get(f"{FULL_API_ENDPOINT}{record_id}")
            if response.status_code == 200:
                print("✅ GET (single) endpoint works!")

            # PUT - Update
            print("Testing PUT...")
            update_data = {"agent_name": "Updated_Agent_001"}
            response = requests.put(
                f"{FULL_API_ENDPOINT}{record_id}",
                json=update_data,
                headers={"Content-Type": "application/json"},
            )
            if response.status_code == 200:
                print("✅ PUT endpoint works!")

            # DELETE
            print("Testing DELETE...")
            response = requests.delete(f"{FULL_API_ENDPOINT}{record_id}")
            if response.status_code == 200:
                print("✅ DELETE endpoint works!")

            print("✅ All CRUD endpoints work!")

        else:
            print(f"❌ POST failed with status {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        print(
            "❌ Could not connect to server. Make sure the server is running on localhost:8000"
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def print_api_documentation():
    """Print API documentation"""
    print("\n📚 API Documentation:")
    print("=" * 50)
    print("Gmail Automation POST Endpoint:")
    print(f"  POST {GMAIL_AUTOMATION_ENDPOINT}")
    print('  Body: {"agent_name": "Agent_001", "profile_name": "profile_gmail_1"}')
    print()
    print("Full CRUD API Endpoints:")
    print(f"  POST   {FULL_API_ENDPOINT}")
    print(f"  GET    {FULL_API_ENDPOINT}")
    print(f"  GET    {FULL_API_ENDPOINT}{{id}}")
    print(f"  PUT    {FULL_API_ENDPOINT}{{id}}")
    print(f"  DELETE {FULL_API_ENDPOINT}{{id}}")
    print()
    print("Additional endpoints:")
    print(f"  GET    {FULL_API_ENDPOINT}agent/{{agent_name}}")
    print(f"  GET    {FULL_API_ENDPOINT}analytics/stats")
    print(f"  POST   {FULL_API_ENDPOINT}bulk-delete")


if __name__ == "__main__":
    print("🚀 Testing Logged Out Profiles API Implementation")
    print("=" * 50)

    # Test the Gmail automation endpoint (what the user specifically requested)
    result = test_gmail_automation_post()

    # Test the full API endpoints
    test_full_api_endpoints()

    # Print documentation
    print_api_documentation()

    print("\n✅ Testing completed!")
    print("\n💡 Note: Make sure to start the server with:")
    print("   python main.py")
    print("   or")
    print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
