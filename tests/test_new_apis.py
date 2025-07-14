import requests
import json
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"


def test_spam_handler_data_api():
    """Test spam handler data API endpoints"""
    print("=== Testing Spam Handler Data API ===")

    # Test data for spam handler
    spam_data = {
        "agent_name": "test_agent",
        "profile_name": "test_profile@gmail.com",
        "sender_email": "spam_sender@example.com",
        "spam_emails_found": 5,
        "moved_to_inbox": 3,
        "total_time_seconds": 45.5,
        "error_occurred": False,
        "error_details": None,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "spam_email_subjects": ["Spam Email 1", "Spam Email 2", "Spam Email 3"],
    }

    # Test POST (create)
    print("1. Testing POST /spam-handler-data")
    response = requests.post(f"{BASE_URL}/spam-handler-data/", json=spam_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        created_entry = response.json()
        print(f"Created entry ID: {created_entry['id']}")
        entry_id = created_entry["id"]
    else:
        print(f"Error: {response.text}")
        return

    # Test GET (list)
    print("\n2. Testing GET /spam-handler-data")
    response = requests.get(f"{BASE_URL}/spam-handler-data/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total entries: {data['total']}")
        print(f"Entries in response: {len(data['items'])}")
    else:
        print(f"Error: {response.text}")

    # Test GET by ID
    print(f"\n3. Testing GET /spam-handler-data/{entry_id}")
    response = requests.get(f"{BASE_URL}/spam-handler-data/{entry_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        entry = response.json()
        print(f"Retrieved entry: {entry['agent_name']} - {entry['profile_name']}")
    else:
        print(f"Error: {response.text}")

    # Test statistics
    print("\n4. Testing GET /spam-handler-data/statistics")
    response = requests.get(f"{BASE_URL}/spam-handler-data/statistics")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"Statistics: {json.dumps(stats, indent=2)}")
    else:
        print(f"Error: {response.text}")


def test_email_processing_data_api():
    """Test email processing data API endpoints"""
    print("\n=== Testing Email Processing Data API ===")

    # Test data for email processing
    email_data = {
        "agent_name": "test_agent",
        "profile_name": "test_profile@gmail.com",
        "sender_email": "newsletter@example.com",
        "email_subject": "Test Newsletter Email",
        "is_opened": True,
        "is_link_clicked": True,
        "is_unsubscribe_clicked": False,
        "is_reply_sent": False,
        "random_website_visited": "https://example.com",
        "random_website_duration_seconds": 30.5,
        "total_duration_seconds": 120.0,
        "error_occurred": False,
        "error_details": None,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    # Test POST (create)
    print("1. Testing POST /email-processing-data")
    response = requests.post(f"{BASE_URL}/email-processing-data/", json=email_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        created_entry = response.json()
        print(f"Created entry ID: {created_entry['id']}")
        entry_id = created_entry["id"]
    else:
        print(f"Error: {response.text}")
        return

    # Test GET (list)
    print("\n2. Testing GET /email-processing-data")
    response = requests.get(f"{BASE_URL}/email-processing-data/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total entries: {data['total']}")
        print(f"Entries in response: {len(data['items'])}")
    else:
        print(f"Error: {response.text}")

    # Test GET by ID
    print(f"\n3. Testing GET /email-processing-data/{entry_id}")
    response = requests.get(f"{BASE_URL}/email-processing-data/{entry_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        entry = response.json()
        print(f"Retrieved entry: {entry['agent_name']} - {entry['email_subject']}")
    else:
        print(f"Error: {response.text}")

    # Test statistics
    print("\n4. Testing GET /email-processing-data/statistics")
    response = requests.get(f"{BASE_URL}/email-processing-data/statistics")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"Statistics: {json.dumps(stats, indent=2)}")
    else:
        print(f"Error: {response.text}")


def main():
    """Run all API tests"""
    print("Starting API Tests...")
    print("=" * 50)

    try:
        test_spam_handler_data_api()
        test_email_processing_data_api()
        print("\n" + "=" * 50)
        print("API Tests Completed!")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error during testing: {str(e)}")


if __name__ == "__main__":
    main()
