import requests
import json

# Test the API endpoint directly
try:
    # Test with 720 hours (30 days) - this matches the frontend default
    response = requests.get(
        "http://localhost:8000/api/v1/quick-actions/real-time-agent-errors?time_filter=720"
    )
    print("=== API Response Status:", response.status_code, "===")

    if response.status_code == 200:
        data = response.json()
        print("Moderate agents count:", len(data.get("moderate_agents", [])))
        print("Severe agents count:", len(data.get("severe_agents", [])))

        print("\nModerate agents:")
        for agent in data.get("moderate_agents", []):
            total = agent["spam_error_count"] + agent["email_error_count"]
            print(
                f'  {agent["name"]}: spam_errors={agent["spam_error_count"]}, email_errors={agent["email_error_count"]}, total={total}'
            )

        print("\nSevere agents:")
        for agent in data.get("severe_agents", []):
            total = agent["spam_error_count"] + agent["email_error_count"]
            print(
                f'  {agent["name"]}: spam_errors={agent["spam_error_count"]}, email_errors={agent["email_error_count"]}, total={total}'
            )
    else:
        print("Error response:", response.text)

except Exception as e:
    print("Error:", str(e))
    print("Make sure the backend server is running on localhost:8000")
