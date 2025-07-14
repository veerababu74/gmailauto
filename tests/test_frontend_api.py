#!/usr/bin/env python3
"""
Test the specific API endpoint that the frontend uses.
"""

import requests


def test_frontend_api():
    base_url = "http://localhost:8000/api/v1/quick-actions"

    print("Testing the frontend API endpoints...")

    # Test the real-time agent errors endpoint (which the frontend uses)
    for time_filter in [24, 168, 720]:
        print(f"\n=== Testing time_filter={time_filter} hours ===")

        try:
            response = requests.get(
                f"{base_url}/real-time-agent-errors?time_filter={time_filter}"
            )

            if response.status_code == 200:
                data = response.json()
                moderate_count = len(data.get("moderate_agents", []))
                severe_count = len(data.get("severe_agents", []))

                print(f"Response successful:")
                print(f"  Moderate agents: {moderate_count}")
                print(f"  Severe agents: {severe_count}")

                # Show sample agents if any
                if moderate_count > 0:
                    print("  Sample moderate agents:")
                    for agent in data["moderate_agents"][:3]:
                        print(
                            f"    {agent['name']}: spam={agent['spam_error_count']}, email={agent['email_error_count']}, total={agent['total_errors']}"
                        )

                if severe_count > 0:
                    print("  Sample severe agents:")
                    for agent in data["severe_agents"][:3]:
                        print(
                            f"    {agent['name']}: spam={agent['spam_error_count']}, email={agent['email_error_count']}, total={agent['total_errors']}"
                        )

            else:
                print(f"Error: HTTP {response.status_code}")
                print(f"Response: {response.text}")

        except Exception as e:
            print(f"Request failed: {e}")


if __name__ == "__main__":
    test_frontend_api()
