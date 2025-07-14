"""
Test script for Gmail Handler Automation APIs
This script demonstrates how to use all the Gmail automation APIs
"""

import requests
import json
from datetime import datetime, timedelta
import time

# Configuration
BASE_URL = "http://localhost:8000/api/v1/gmail-automation"
AUTH_TOKEN = "your_jwt_token_here"  # Replace with actual JWT token

# Headers for authenticated requests
HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}", "Content-Type": "application/json"}


class GmailAutomationAPITester:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def test_health_check(self):
        """Test the health check endpoint"""
        print("🔍 Testing Health Check...")
        response = requests.get(f"{self.base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)

    def test_random_urls(self):
        """Test Random URLs endpoints"""
        print("🌐 Testing Random URLs APIs...")

        # Create a random URL
        create_data = {
            "url": "https://example.com",
            "description": "Test website for automation",
            "category": "test",
            "is_active": True,
        }

        response = requests.post(
            f"{self.base_url}/random-urls", headers=self.headers, json=create_data
        )
        print(f"Create URL - Status: {response.status_code}")
        if response.status_code == 200:
            created_url = response.json()
            print(f"Created URL ID: {created_url['id']}")

            # Get all URLs
            response = requests.get(
                f"{self.base_url}/random-urls", headers=self.headers
            )
            print(f"Get URLs - Status: {response.status_code}")
            print(f"Total URLs: {response.json().get('total', 0)}")

            # Get active URLs
            response = requests.get(
                f"{self.base_url}/random-urls/active", headers=self.headers
            )
            print(f"Get Active URLs - Status: {response.status_code}")
            print(f"Active URLs Count: {len(response.json())}")

            # Update URL
            update_data = {
                "description": "Updated test website",
                "category": "updated-test",
            }
            response = requests.put(
                f"{self.base_url}/random-urls/{created_url['id']}",
                headers=self.headers,
                json=update_data,
            )
            print(f"Update URL - Status: {response.status_code}")

            # Delete URL
            response = requests.delete(
                f"{self.base_url}/random-urls/{created_url['id']}", headers=self.headers
            )
            print(f"Delete URL - Status: {response.status_code}")

        print("-" * 50)

    def test_default_senders(self):
        """Test Default Senders endpoints"""
        print("📧 Testing Default Senders APIs...")

        # Create a default sender
        create_data = {
            "email": "test@example.com",
            "description": "Test sender for automation",
            "is_active": True,
        }

        response = requests.post(
            f"{self.base_url}/default-senders", headers=self.headers, json=create_data
        )
        print(f"Create Sender - Status: {response.status_code}")
        if response.status_code == 200:
            created_sender = response.json()
            print(f"Created Sender ID: {created_sender['id']}")

            # Get all senders
            response = requests.get(
                f"{self.base_url}/default-senders", headers=self.headers
            )
            print(f"Get Senders - Status: {response.status_code}")
            print(f"Total Senders: {response.json().get('total', 0)}")

            # Delete sender
            response = requests.delete(
                f"{self.base_url}/default-senders/{created_sender['id']}",
                headers=self.headers,
            )
            print(f"Delete Sender - Status: {response.status_code}")

        print("-" * 50)

    def test_connectivity_settings(self):
        """Test Connectivity Settings endpoints"""
        print("🔗 Testing Connectivity Settings APIs...")

        # Create a connectivity setting
        create_data = {
            "setting_name": "test_proxy",
            "setting_value": "proxy.test.com:8080",
            "description": "Test proxy server",
            "is_active": True,
        }

        response = requests.post(
            f"{self.base_url}/connectivity-settings",
            headers=self.headers,
            json=create_data,
        )
        print(f"Create Setting - Status: {response.status_code}")
        if response.status_code == 200:
            created_setting = response.json()
            print(f"Created Setting ID: {created_setting['id']}")

            # Get all settings
            response = requests.get(
                f"{self.base_url}/connectivity-settings", headers=self.headers
            )
            print(f"Get Settings - Status: {response.status_code}")
            print(f"Total Settings: {response.json().get('total', 0)}")

            # Delete setting
            response = requests.delete(
                f"{self.base_url}/connectivity-settings/{created_setting['id']}",
                headers=self.headers,
            )
            print(f"Delete Setting - Status: {response.status_code}")

        print("-" * 50)

    def test_spam_handler_data(self):
        """Test Spam Handler Data endpoints"""
        print("🛡️ Testing Spam Handler Data APIs...")

        # Create spam handler data
        create_data = {
            "agent_name": "TestAgent_001",
            "profile_name": "test_profile",
            "sender_email": "test@gmail.com",
            "spam_emails_found": 10,
            "moved_to_inbox": 8,
            "total_time_seconds": 45.5,
            "error_occurred": False,
            "spam_email_subjects": ["Test spam email 1", "Test spam email 2"],
        }

        response = requests.post(
            f"{self.base_url}/spam-handler-data", headers=self.headers, json=create_data
        )
        print(f"Create Spam Data - Status: {response.status_code}")
        if response.status_code == 200:
            created_data = response.json()
            print(f"Created Spam Data ID: {created_data['id']}")

            # Get all spam data
            response = requests.get(
                f"{self.base_url}/spam-handler-data", headers=self.headers
            )
            print(f"Get Spam Data - Status: {response.status_code}")
            print(f"Total Spam Data: {response.json().get('total', 0)}")

            # Get specific spam data
            response = requests.get(
                f"{self.base_url}/spam-handler-data/{created_data['id']}",
                headers=self.headers,
            )
            print(f"Get Specific Spam Data - Status: {response.status_code}")

            # Delete spam data
            response = requests.delete(
                f"{self.base_url}/spam-handler-data/{created_data['id']}",
                headers=self.headers,
            )
            print(f"Delete Spam Data - Status: {response.status_code}")

        print("-" * 50)

    def test_email_processing_data(self):
        """Test Email Processing Data endpoints"""
        print("📨 Testing Email Processing Data APIs...")

        # Create email processing data
        create_data = {
            "agent_name": "TestAgent_001",
            "profile_name": "test_profile",
            "sender_email": "test@gmail.com",
            "email_subject": "Test Newsletter",
            "is_opened": True,
            "is_link_clicked": True,
            "is_unsubscribe_clicked": False,
            "is_reply_sent": False,
            "random_website_visited": "https://test-site.com",
            "random_website_duration_seconds": 120.5,
            "total_duration_seconds": 180.7,
            "error_occurred": False,
        }

        response = requests.post(
            f"{self.base_url}/email-processing-data",
            headers=self.headers,
            json=create_data,
        )
        print(f"Create Email Data - Status: {response.status_code}")
        if response.status_code == 200:
            created_data = response.json()
            print(f"Created Email Data ID: {created_data['id']}")

            # Get all email data
            response = requests.get(
                f"{self.base_url}/email-processing-data", headers=self.headers
            )
            print(f"Get Email Data - Status: {response.status_code}")
            print(f"Total Email Data: {response.json().get('total', 0)}")

            # Delete email data
            response = requests.delete(
                f"{self.base_url}/email-processing-data/{created_data['id']}",
                headers=self.headers,
            )
            print(f"Delete Email Data - Status: {response.status_code}")

        print("-" * 50)

    def test_analytics(self):
        """Test Analytics endpoints"""
        print("📊 Testing Analytics APIs...")

        # Get spam handler stats
        response = requests.get(
            f"{self.base_url}/analytics/spam-handler-stats", headers=self.headers
        )
        print(f"Spam Handler Stats - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Stats: {json.dumps(response.json(), indent=2)}")

        # Get email processing stats
        response = requests.get(
            f"{self.base_url}/analytics/email-processing-stats", headers=self.headers
        )
        print(f"Email Processing Stats - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Stats: {json.dumps(response.json(), indent=2)}")

        print("-" * 50)

    def test_bulk_operations(self):
        """Test Bulk Operations"""
        print("🔄 Testing Bulk Operations...")

        # Create multiple URLs for bulk delete test
        url_ids = []
        for i in range(3):
            create_data = {
                "url": f"https://test{i}.com",
                "description": f"Test URL {i}",
                "category": "bulk-test",
                "is_active": True,
            }
            response = requests.post(
                f"{self.base_url}/random-urls", headers=self.headers, json=create_data
            )
            if response.status_code == 200:
                url_ids.append(response.json()["id"])

        if url_ids:
            # Bulk delete
            bulk_delete_data = {"ids": url_ids}
            response = requests.post(
                f"{self.base_url}/random-urls/bulk-delete",
                headers=self.headers,
                json=bulk_delete_data,
            )
            print(f"Bulk Delete URLs - Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(
                    f"Deleted: {result['deleted_count']}, Failed: {result['failed_ids']}"
                )

        print("-" * 50)

    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Gmail Automation API Tests...\n")

        try:
            self.test_health_check()
            self.test_random_urls()
            self.test_default_senders()
            self.test_connectivity_settings()
            self.test_spam_handler_data()
            self.test_email_processing_data()
            self.test_analytics()
            self.test_bulk_operations()

            print("✅ All tests completed!")

        except requests.exceptions.ConnectionError:
            print(
                "❌ Connection Error: Make sure the API server is running at",
                self.base_url,
            )
        except requests.exceptions.RequestException as e:
            print(f"❌ Request Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")


def main():
    """Main function to run tests"""
    print("Gmail Handler Automation API Tester")
    print("=" * 50)

    # Note: Replace AUTH_TOKEN with actual JWT token for authenticated tests
    if AUTH_TOKEN == "your_jwt_token_here":
        print(
            "⚠️  Warning: Please update AUTH_TOKEN with a valid JWT token for full testing"
        )
        print("Some tests may fail without proper authentication\n")

    tester = GmailAutomationAPITester(BASE_URL, HEADERS)
    tester.run_all_tests()


if __name__ == "__main__":
    main()
