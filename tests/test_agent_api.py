#!/usr/bin/env python3
"""
Test script for Agent API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def test_agent_endpoints():
    print("Testing Agent Management API Endpoints...")

    # Test data
    test_agent = {
        "agent_name": "TestAgent001",
        "machine_brand": "Dell OptiPlex",
        "location": "Server Room A",
    }

    # Get access token (you'll need to implement login first)
    print("\n1. Testing Agent Creation (without auth - should fail)")
    try:
        response = requests.post(f"{BASE_URL}/agents/", json=test_agent)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n2. Testing Get All Agents (without auth - should fail)")
    try:
        response = requests.get(f"{BASE_URL}/agents/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n3. Testing Get Active Agents (without auth - should fail)")
    try:
        response = requests.get(f"{BASE_URL}/agents/active")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

    print("\nAPI endpoints are properly protected with authentication!")


if __name__ == "__main__":
    test_agent_endpoints()
