"""
Test the client methods against the new APIs
"""

import sys
import os
import datetime
from typing import List, Dict

# Add the utils directory to the path to import the api_client
utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils"))
sys.path.insert(0, utils_path)

from api_client import APIClient


def test_client_methods():
    """Test the client methods for posting data to the APIs"""

    # Initialize the API client
    client = APIClient()

    print("=== Testing API Client Methods ===")

    # Test spam data posting
    print("\n1. Testing post_spam_data method")
    spam_emails_found = [
        {"subject": "Win $1000 Now!", "sender": "scammer@fake.com"},
        {"subject": "Free Viagra!", "sender": "spam@pills.com"},
        {"subject": "Nigerian Prince Money", "sender": "prince@nigeria.fake"},
    ]

    result = client.post_spam_data(
        profile_name="test_profile@gmail.com",
        sender_email="spammer@example.com",
        spam_emails_found=spam_emails_found,
        moved_to_inbox=2,
        total_time=67.8,
        error_occurred=False,
        error_details=None,
    )

    print(f"Spam data posting result: {result}")

    # Test email processing data posting
    print("\n2. Testing post_email_processing_data method")
    result = client.post_email_processing_data(
        profile_name="test_profile@gmail.com",
        sender_email="newsletter@company.com",
        email_subject="Weekly Newsletter - July 2025",
        is_opened=True,
        is_link_clicked=True,
        is_unsubscribe_clicked=False,
        is_reply_sent=True,
        random_website_visited="https://example.com/blog",
        random_website_duration=45.2,
        total_duration=125.7,
        error_occurred=False,
        error_details=None,
    )

    print(f"Email processing data posting result: {result}")

    # Test error case for spam data
    print("\n3. Testing post_spam_data with error")
    result = client.post_spam_data(
        profile_name="test_profile@gmail.com",
        sender_email="problematic@example.com",
        spam_emails_found=[{"subject": "Test", "sender": "test@test.com"}],
        moved_to_inbox=0,
        total_time=15.3,
        error_occurred=True,
        error_details="Failed to move emails due to authentication error",
    )

    print(f"Spam data with error posting result: {result}")

    # Test error case for email processing
    print("\n4. Testing post_email_processing_data with error")
    result = client.post_email_processing_data(
        profile_name="test_profile@gmail.com",
        sender_email="broken@example.com",
        email_subject="Test Email That Failed",
        is_opened=False,
        is_link_clicked=False,
        is_unsubscribe_clicked=False,
        is_reply_sent=False,
        random_website_visited=None,
        random_website_duration=0,
        total_duration=5.1,
        error_occurred=True,
        error_details="Browser crashed during email processing",
    )

    print(f"Email processing with error posting result: {result}")

    print("\n=== API Client Testing Complete ===")


if __name__ == "__main__":
    test_client_methods()
