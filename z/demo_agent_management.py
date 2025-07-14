#!/usr/bin/env python3
"""
Demo script to create test data for Agent Management
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def create_test_user():
    """Create a test user for demonstration"""
    user_data = {
        "email": "testuser@example.com",
        "password": "TestPassword123!",
        "name": "Test User",
    }

    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        print(f"User registration: {response.status_code}")
        if response.status_code != 200:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error creating user: {e}")
        return False


def login_user():
    """Login and get access token"""
    login_data = {"username": "testuser@example.com", "password": "TestPassword123!"}

    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        print(f"Login status: {response.status_code}")
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"Login failed: {response.json()}")
            return None
    except Exception as e:
        print(f"Error logging in: {e}")
        return None


def test_agent_crud(token):
    """Test CRUD operations for agents"""
    headers = {"Authorization": f"Bearer {token}"}

    # Create agents
    agents = [
        {
            "agent_name": "ProductionAgent01",
            "machine_brand": "Dell OptiPlex 7090",
            "location": "Data Center Room A",
        },
        {
            "agent_name": "TestAgent01",
            "machine_brand": "HP EliteDesk 800",
            "location": "Development Office",
        },
        {
            "agent_name": "BackupAgent01",
            "machine_brand": "Lenovo ThinkCentre",
            "location": "Backup Server Room",
        },
    ]

    created_agents = []

    print("\n=== Creating Agents ===")
    for agent_data in agents:
        try:
            response = requests.post(
                f"{BASE_URL}/agents/", json=agent_data, headers=headers
            )
            print(f"Created agent '{agent_data['agent_name']}': {response.status_code}")
            if response.status_code == 201:
                created_agents.append(response.json())
            else:
                print(f"Error: {response.json()}")
        except Exception as e:
            print(f"Error creating agent: {e}")

    print(f"\n=== Successfully created {len(created_agents)} agents ===")

    # Get all agents
    print("\n=== Getting All Agents ===")
    try:
        response = requests.get(f"{BASE_URL}/agents/", headers=headers)
        if response.status_code == 200:
            agents_list = response.json()
            print(f"Total agents: {len(agents_list)}")
            for agent in agents_list:
                print(
                    f"- {agent['agent_name']} ({agent['machine_brand']}) at {agent['location']}"
                )
        else:
            print(f"Error getting agents: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

    # Update an agent
    if created_agents:
        print("\n=== Updating Agent ===")
        agent_to_update = created_agents[0]
        update_data = {"location": "Updated Location - Server Room B"}
        try:
            response = requests.put(
                f"{BASE_URL}/agents/{agent_to_update['id']}",
                json=update_data,
                headers=headers,
            )
            print(f"Updated agent: {response.status_code}")
            if response.status_code == 200:
                updated_agent = response.json()
                print(f"New location: {updated_agent['location']}")
        except Exception as e:
            print(f"Error updating agent: {e}")

    # Delete an agent (soft delete)
    if len(created_agents) > 1:
        print("\n=== Deleting Agent ===")
        agent_to_delete = created_agents[1]
        try:
            response = requests.delete(
                f"{BASE_URL}/agents/{agent_to_delete['id']}", headers=headers
            )
            print(f"Deleted agent: {response.status_code}")
            if response.status_code == 200:
                deleted_agent = response.json()
                print(
                    f"Agent '{deleted_agent['agent_name']}' is now inactive: {not deleted_agent['is_active']}"
                )
        except Exception as e:
            print(f"Error deleting agent: {e}")


def main():
    print("=== Agent Management Demo ===")

    # Create test user
    print("\n1. Creating test user...")
    if not create_test_user():
        print("User might already exist, trying to login...")

    # Login
    print("\n2. Logging in...")
    token = login_user()
    if not token:
        print("Failed to login. Exiting.")
        return

    # Test agent CRUD operations
    print("\n3. Testing Agent CRUD operations...")
    test_agent_crud(token)

    print("\n=== Demo Complete ===")
    print("You can now:")
    print("1. Open the frontend at http://localhost:5173")
    print("2. Login with testuser@example.com / TestPassword123!")
    print("3. Navigate to 'Agent Management' to see the agents")
    print("4. Test creating, editing, and deleting agents through the UI")


if __name__ == "__main__":
    main()
