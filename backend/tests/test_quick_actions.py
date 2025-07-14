#!/usr/bin/env python3
"""
Test script to verify the quick actions API endpoints
"""
import requests
import json

API_BASE_URL = "http://localhost:8000/api/v1"


def test_quick_actions_endpoints():
    print("Testing Quick Actions API endpoints...")

    # Test error summary endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/quick-actions/error-summary")
        print(f"Error Summary endpoint: {response.status_code}")
        if response.status_code == 200:
            print("✓ Error Summary endpoint working")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"✗ Error Summary endpoint failed: {response.text}")
    except Exception as e:
        print(f"✗ Error Summary endpoint error: {e}")

    print("\n" + "=" * 50 + "\n")

    # Test agent error levels endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/quick-actions/agent-error-levels")
        print(f"Agent Error Levels endpoint: {response.status_code}")
        if response.status_code == 200:
            print("✓ Agent Error Levels endpoint working")
            data = response.json()
            print(f"Moderate agents: {len(data.get('moderate_agents', []))}")
            print(f"Severe agents: {len(data.get('severe_agents', []))}")
        else:
            print(f"✗ Agent Error Levels endpoint failed: {response.text}")
    except Exception as e:
        print(f"✗ Agent Error Levels endpoint error: {e}")

    print("\n" + "=" * 50 + "\n")

    # Test basic health check
    try:
        response = requests.get(f"{API_BASE_URL}/../health")
        print(f"Health Check endpoint: {response.status_code}")
        if response.status_code == 200:
            print("✓ Backend is healthy")
            print(response.json())
        else:
            print(f"✗ Health check failed: {response.text}")
    except Exception as e:
        print(f"✗ Health check error: {e}")


if __name__ == "__main__":
    test_quick_actions_endpoints()
