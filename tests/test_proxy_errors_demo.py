"""
Test script for Proxy Error endpoints
This script demonstrates the CRUD operations for proxy errors.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
GMAIL_AUTOMATION_URL = "http://localhost:8000/api/v1/gmail-automation"


def test_proxy_error_endpoints():
    """Test the proxy error endpoints"""

    # Sample proxy error data
    proxy_error_data = {
        "agent_name": "test_agent_001",
        "proxy": "192.168.1.100:8080",
        "error_details": "Connection timeout after 30 seconds. The proxy server did not respond.",
        "profile_name": "gmail_profile_001",
    }

    print("=== Testing Proxy Error Endpoints ===\n")

    # Note: These tests require the server to be running and proper authentication
    # This is a demonstration of the API structure and expected payloads

    print("1. Create Proxy Error (POST /api/v1/proxy-errors/)")
    print("Request payload:")
    print(json.dumps(proxy_error_data, indent=2))
    print(
        "\nExpected response: 201 Created with proxy error object including ID and timestamps\n"
    )

    print("2. Get All Proxy Errors (GET /api/v1/proxy-errors/)")
    print("Query parameters: ?skip=0&limit=10&agent_name=test_agent")
    print("Expected response: Paginated list of proxy errors\n")

    print("3. Get Proxy Error by ID (GET /api/v1/proxy-errors/{id})")
    print("Expected response: Single proxy error object\n")

    print("4. Update Proxy Error (PUT /api/v1/proxy-errors/{id})")
    update_data = {
        "error_details": "Updated: Connection timeout - proxy server unreachable"
    }
    print("Request payload:")
    print(json.dumps(update_data, indent=2))
    print("Expected response: Updated proxy error object\n")

    print("5. Get Proxy Errors by Agent (GET /api/v1/proxy-errors/agent/{agent_name})")
    print("Expected response: List of recent proxy errors for the agent\n")

    print(
        "6. Get Proxy Error Count (GET /api/v1/proxy-errors/proxy/{proxy_address}/count)"
    )
    print("Expected response: {'proxy': '192.168.1.100:8080', 'error_count': 5}\n")

    print("7. Delete Proxy Error (DELETE /api/v1/proxy-errors/{id})")
    print("Expected response: Deleted proxy error object\n")


def test_gmail_automation_proxy_errors():
    """Test the Gmail automation proxy error endpoints"""

    print("=== Testing Gmail Automation Proxy Error Endpoints ===\n")

    # Sample proxy error data
    proxy_error_data = {
        "agent_name": "gmail_agent_001",
        "proxy": "proxy.example.com:3128",
        "error_details": "SOCKS5 proxy authentication failed",
        "profile_name": "premium_gmail_profile",
    }

    print("1. Create Proxy Error (POST /api/v1/gmail-automation/proxy-errors)")
    print("Request payload:")
    print(json.dumps(proxy_error_data, indent=2))
    print("\nExpected response: 201 Created with proxy error object\n")

    print("2. Get All Proxy Errors (GET /api/v1/gmail-automation/proxy-errors)")
    print("Query parameters: ?skip=0&limit=100&search=authentication")
    print("Expected response: Paginated list with search filtering\n")

    print(
        "3. Get Recent Errors by Agent (GET /api/v1/gmail-automation/proxy-errors/agent/gmail_agent_001)"
    )
    print("Query parameters: ?limit=5")
    print("Expected response: List of 5 most recent errors for the agent\n")


def demonstrate_api_usage():
    """Demonstrate typical API usage patterns"""

    print("=== Common Usage Patterns ===\n")

    print("1. Error Logging Pattern:")
    print("   When a proxy fails, create an error record:")
    print("   POST /api/v1/proxy-errors/ or /api/v1/gmail-automation/proxy-errors")
    print("   Include agent_name, proxy, error_details, and profile_name\n")

    print("2. Monitoring Pattern:")
    print("   Check recent errors for an agent:")
    print("   GET /api/v1/proxy-errors/agent/{agent_name}?limit=10\n")

    print("3. Proxy Health Check Pattern:")
    print("   Count errors for a specific proxy:")
    print("   GET /api/v1/proxy-errors/proxy/{proxy_address}/count\n")

    print("4. Filtering and Search Pattern:")
    print("   Search for specific error types:")
    print("   GET /api/v1/proxy-errors/?search=timeout&limit=50\n")

    print("5. Cleanup Pattern:")
    print("   Delete old error records:")
    print("   DELETE /api/v1/proxy-errors/{id}\n")


if __name__ == "__main__":
    print("Proxy Error API Test and Demonstration Script")
    print("=" * 50)
    print()

    test_proxy_error_endpoints()
    print("\n" + "=" * 50 + "\n")

    test_gmail_automation_proxy_errors()
    print("\n" + "=" * 50 + "\n")

    demonstrate_api_usage()

    print("\nNote: To actually test these endpoints, start the server with:")
    print("python run_server.py")
    print("\nThen use tools like curl, Postman, or create a proper test client.")
