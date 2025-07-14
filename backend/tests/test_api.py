import requests
import json

# Test the FastAPI backend endpoints
BASE_URL = "http://localhost:8000/api/v1"


def test_health_check():
    """Test the health endpoint"""
    response = requests.get("http://localhost:8000/health")
    print(f"Health Check: {response.status_code} - {response.json()}")


def test_login():
    """Test login with demo credentials"""
    login_data = {"email": "admin@gmail.com", "password": "admin123"}

    response = requests.post(f"{BASE_URL}/auth/login/json", json=login_data)
    print(f"Login: {response.status_code} - {response.json()}")

    if response.status_code == 200:
        return response.json()["access_token"]
    return None


def test_authenticated_endpoints(token):
    """Test authenticated endpoints"""
    headers = {"Authorization": f"Bearer {token}"}

    # Test get current user
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print(f"Get Current User: {response.status_code} - {response.json()}")

    # Test create client
    client_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "company": "Example Corp",
        "status": "active",
    }

    response = requests.post(f"{BASE_URL}/clients/", json=client_data, headers=headers)
    print(f"Create Client: {response.status_code} - {response.json()}")

    # Test get clients
    response = requests.get(f"{BASE_URL}/clients/", headers=headers)
    print(f"Get Clients: {response.status_code} - {response.json()}")

    # Test get client stats
    response = requests.get(f"{BASE_URL}/clients/stats", headers=headers)
    print(f"Client Stats: {response.status_code} - {response.json()}")


def main():
    print("Testing FastAPI Backend...")
    print("=" * 50)

    try:
        test_health_check()
        token = test_login()

        if token:
            print(f"Authentication successful! Token: {token[:20]}...")
            test_authenticated_endpoints(token)
        else:
            print("Authentication failed!")

    except requests.exceptions.ConnectionError:
        print(
            "Error: Could not connect to the server. Make sure it's running on http://localhost:8000"
        )
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
