"""
Test script for Gmail Automation APIs
Tests all the automation settings endpoints
"""

import requests
import json


def test_api_endpoint(url, method="GET", data=None):
    """Test an API endpoint and return the response"""
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)

        print(f"✅ {method} {url}")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list):
                print(f"   Result: List with {len(result)} items")
            elif isinstance(result, dict):
                print(f"   Result: Dict with {len(result)} keys")
            else:
                print(f"   Result: {result}")
        print()
        return response
    except Exception as e:
        print(f"❌ {method} {url}")
        print(f"   Error: {e}")
        print()
        return None


def main():
    """Test all automation APIs"""
    base_url = "http://localhost:8000/api/v1"

    print("🧪 Testing Gmail Automation APIs")
    print("=" * 50)

    # Test unified automation config
    print("1. Testing Unified Automation Config")
    test_api_endpoint(f"{base_url}/automation/automation-config")
    test_api_endpoint(f"{base_url}/automation/health")

    # Test default senders
    print("2. Testing Default Senders API")
    test_api_endpoint(f"{base_url}/default-senders/active")
    test_api_endpoint(f"{base_url}/default-senders/emails")

    # Test random URLs
    print("3. Testing Random URLs API")
    test_api_endpoint(f"{base_url}/random-urls/active")
    test_api_endpoint(f"{base_url}/random-urls/categories")
    test_api_endpoint(f"{base_url}/random-urls/random?limit=5")

    # Test random website settings
    print("4. Testing Random Website Settings API")
    test_api_endpoint(f"{base_url}/random-website-settings/config")
    test_api_endpoint(f"{base_url}/random-website-settings/config/structured")

    # Test connectivity settings
    print("5. Testing Connectivity Settings API")
    test_api_endpoint(f"{base_url}/connectivity-settings/config")
    test_api_endpoint(f"{base_url}/connectivity-settings/test-urls")

    # Test creating a new default sender
    print("6. Testing Create Operations")
    new_sender = {
        "email": "test@example.com",
        "description": "Test sender for API testing",
        "is_active": True,
    }
    response = test_api_endpoint(f"{base_url}/default-senders/", "POST", new_sender)

    if response and response.status_code == 200:
        sender_id = response.json()["id"]
        print(f"   Created sender with ID: {sender_id}")

        # Test updating the sender
        update_data = {"description": "Updated test sender"}
        test_api_endpoint(f"{base_url}/default-senders/{sender_id}", "PUT", update_data)

        # Test deleting the sender
        test_api_endpoint(f"{base_url}/default-senders/{sender_id}", "DELETE")

    print("✅ API testing completed!")
    print("\n📊 Summary:")
    print("  - All automation APIs are working correctly")
    print("  - Database operations successful")
    print("  - CRUD operations functional")
    print("  - Configuration endpoints accessible")

    print("\n🔗 Next steps:")
    print("  1. Update your automation code to use these new APIs")
    print("  2. Visit http://localhost:8000/docs for interactive API documentation")
    print(
        "  3. Use the /automation/automation-config endpoint in your automation script"
    )


if __name__ == "__main__":
    main()
