#!/usr/bin/env python3

import requests
import json


def test_timeframe(hours, label):
    try:
        print(f"\n=== Testing {label} ({hours} hours) ===")
        url = f"http://localhost:8000/api/v1/quick-actions/real-time-agent-errors?time_filter={hours}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            moderate_count = data.get("total_moderate", 0)
            severe_count = data.get("total_severe", 0)

            print(f"Moderate agents: {moderate_count}")
            print(f"Severe agents: {severe_count}")

            # Show some details for moderate agents
            moderate_agents = data.get("moderate_agents", [])
            if moderate_agents:
                print("Sample moderate agents:")
                for agent in moderate_agents[:3]:  # Show first 3
                    print(
                        f"  {agent['name']}: spam_errors={agent['spam_error_count']}, email_errors={agent['email_error_count']}, total={agent['total_errors']}"
                    )

            # Show some details for severe agents
            severe_agents = data.get("severe_agents", [])
            if severe_agents:
                print("Sample severe agents:")
                for agent in severe_agents[:3]:  # Show first 3
                    print(
                        f"  {agent['name']}: spam_errors={agent['spam_error_count']}, email_errors={agent['email_error_count']}, total={agent['total_errors']}"
                    )
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Test all timeframes
    test_timeframe(24, "24 Hours")
    test_timeframe(168, "7 Days")
    test_timeframe(720, "30 Days")
