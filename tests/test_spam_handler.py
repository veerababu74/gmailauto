import requests
import json
from datetime import datetime

# Test just the spam handler API
BASE_URL = "http://localhost:8000/api/v1"

spam_data = {
    "agent_name": "test_agent",
    "profile_name": "test_profile@gmail.com",
    "sender_email": "spam_sender@example.com",
    "spam_emails_found": 5,
    "moved_to_inbox": 3,
    "total_time_seconds": 45.5,
    "error_occurred": False,
    "error_details": None,
    "timestamp": datetime.now().isoformat() + "Z",
    "spam_email_subjects": ["Spam Email 1", "Spam Email 2", "Spam Email 3"],
}

print("Testing spam handler data API...")
print(f"Data to send: {json.dumps(spam_data, indent=2)}")

response = requests.post(f"{BASE_URL}/spam-handler-data/", json=spam_data)
print(f"\nPOST Response Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    # Now test GET
    response = requests.get(f"{BASE_URL}/spam-handler-data/")
    print(f"\nGET Response Status: {response.status_code}")
    print(f"Response: {response.text}")
