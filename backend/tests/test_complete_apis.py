"""
Test the new APIs with the exact data structure from the client methods
"""

import requests
import json
import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"


def test_spam_data_structure():
    """Test with the exact structure that the post_spam_data method would send"""
    print("=== Testing Spam Handler Data with Client Structure ===")

    # Data structure from the client's post_spam_data method
    spam_emails_found = [
        {"subject": "Win $1000 Now!", "sender": "scammer@fake.com"},
        {"subject": "Free Viagra!", "sender": "spam@pills.com"},
        {"subject": "Nigerian Prince Money", "sender": "prince@nigeria.fake"},
    ]

    data = {
        "agent_name": "DESKTOP-ABC123",  # machine_name from client
        "profile_name": "test_profile@gmail.com",
        "sender_email": "spammer@example.com",
        "spam_emails_found": len(spam_emails_found),
        "moved_to_inbox": 2,
        "total_time_seconds": 67.8,
        "error_occurred": False,
        "error_details": None,
        "timestamp": datetime.datetime.now().isoformat() + "Z",
        "spam_email_subjects": [
            email.get("subject", "Unknown") for email in spam_emails_found
        ],
    }

    print(f"Sending data: {json.dumps(data, indent=2)}")
    response = requests.post(f"{BASE_URL}/spam-handler-data/", json=data)
    print(f"Response Status: {response.status_code}")
    print(f"Response: {response.text[:200]}...")

    return response.status_code == 200


def test_email_processing_structure():
    """Test with the exact structure that the post_email_processing_data method would send"""
    print("\n=== Testing Email Processing Data with Client Structure ===")

    # Data structure from the client's post_email_processing_data method
    data = {
        "agent_name": "DESKTOP-ABC123",  # machine_name from client
        "profile_name": "test_profile@gmail.com",
        "sender_email": "newsletter@company.com",
        "email_subject": "Weekly Newsletter - July 2025",
        "is_opened": True,
        "is_link_clicked": True,
        "is_unsubscribe_clicked": False,
        "is_reply_sent": True,
        "random_website_visited": "https://example.com/blog",
        "random_website_duration_seconds": 45.2,
        "total_duration_seconds": 125.7,
        "error_occurred": False,
        "error_details": None,
        "timestamp": datetime.datetime.now().isoformat() + "Z",
    }

    print(f"Sending data: {json.dumps(data, indent=2)}")
    response = requests.post(f"{BASE_URL}/email-processing-data/", json=data)
    print(f"Response Status: {response.status_code}")
    print(f"Response: {response.text[:200]}...")

    return response.status_code == 200


def test_api_endpoints():
    """Test various API endpoints"""
    print("\n=== Testing Additional API Endpoints ===")

    # Test statistics endpoints
    print("\n1. Testing spam handler statistics")
    response = requests.get(f"{BASE_URL}/spam-handler-data/statistics")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"Total entries: {stats.get('total_spam_processed', 0)}")

    print("\n2. Testing email processing statistics")
    response = requests.get(f"{BASE_URL}/email-processing-data/statistics")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"Total emails processed: {stats.get('total_emails_processed', 0)}")
        print(f"Open rate: {stats.get('success_rate', 0)}%")

    # Test filtering
    print("\n3. Testing filtering by agent")
    response = requests.get(f"{BASE_URL}/spam-handler-data/?agent_name=DESKTOP-ABC123")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Filtered entries: {data.get('total', 0)}")

    print("\n4. Testing recent entries")
    response = requests.get(f"{BASE_URL}/email-processing-data/recent?hours=24")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        entries = response.json()
        print(f"Recent entries: {len(entries)}")


def main():
    """Run all tests"""
    print("Testing New APIs with Client Data Structures")
    print("=" * 60)

    try:
        # Test both data structures
        spam_success = test_spam_data_structure()
        email_success = test_email_processing_structure()

        # Test additional endpoints
        test_api_endpoints()

        print("\n" + "=" * 60)
        print("Test Results:")
        print(f"Spam Handler API: {'✓ PASS' if spam_success else '✗ FAIL'}")
        print(f"Email Processing API: {'✓ PASS' if email_success else '✗ FAIL'}")

        if spam_success and email_success:
            print("\n🎉 All APIs are working correctly!")
            print("The backend is ready to receive data from the client methods.")
        else:
            print("\n❌ Some APIs failed. Check the error messages above.")

    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")


if __name__ == "__main__":
    main()
