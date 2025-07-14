#!/usr/bin/env python3
"""
Debug script to understand why agents aren't being classified as moderate for 30 days.
"""


def test_categorization():
    # Test the exact logic from the API

    # Sample agent data from the test results
    agents = [
        {"name": "BackupAgent01", "spam_errors": 7, "email_errors": 9, "total": 16},
        {
            "name": "Gmail-Agent-ATL-006",
            "spam_errors": 7,
            "email_errors": 9,
            "total": 16,
        },
        {
            "name": "Gmail-Agent-CHI-003",
            "spam_errors": 3,
            "email_errors": 14,
            "total": 17,
        },
    ]

    time_filter = 720  # 30 days

    # Updated thresholds (after our fix)
    if time_filter <= 24:  # 24 hours
        severe_threshold = 15
        moderate_threshold = 5
        spam_severe_threshold = 8
        email_severe_threshold = 8
    elif time_filter <= 168:  # 7 days
        severe_threshold = 35  # ~5 errors per day
        moderate_threshold = 10  # ~1.5 errors per day
        spam_severe_threshold = 15
        email_severe_threshold = 15
    else:  # 30 days and beyond
        severe_threshold = 50  # ~1.7 errors per day
        moderate_threshold = 15  # ~0.5 errors per day
        spam_severe_threshold = 25
        email_severe_threshold = 25

    print(f"Thresholds for {time_filter} hours:")
    print(f"  severe_threshold: {severe_threshold}")
    print(f"  moderate_threshold: {moderate_threshold}")
    print(f"  spam_severe_threshold: {spam_severe_threshold}")
    print(f"  email_severe_threshold: {email_severe_threshold}")
    print()

    moderate_agents = []
    severe_agents = []

    for agent in agents:
        spam_error_count = agent["spam_errors"]
        email_error_count = agent["email_errors"]
        total_errors = agent["total"]

        print(f"Agent: {agent['name']}")
        print(
            f"  spam_errors: {spam_error_count}, email_errors: {email_error_count}, total: {total_errors}"
        )

        # Test severe condition
        severe_condition_1 = total_errors >= severe_threshold
        severe_condition_2a = spam_error_count >= spam_severe_threshold
        severe_condition_2b = email_error_count >= email_severe_threshold
        severe_condition_2 = severe_condition_2a and severe_condition_2b
        is_severe = severe_condition_1 or severe_condition_2

        print(f"  Severe checks:")
        print(
            f"    total_errors >= severe_threshold: {total_errors} >= {severe_threshold} = {severe_condition_1}"
        )
        print(
            f"    spam_errors >= spam_severe_threshold: {spam_error_count} >= {spam_severe_threshold} = {severe_condition_2a}"
        )
        print(
            f"    email_errors >= email_severe_threshold: {email_error_count} >= {email_severe_threshold} = {severe_condition_2b}"
        )
        print(
            f"    Both spam and email severe: {severe_condition_2a} AND {severe_condition_2b} = {severe_condition_2}"
        )
        print(
            f"    Overall severe: {severe_condition_1} OR {severe_condition_2} = {is_severe}"
        )

        if is_severe:
            severe_agents.append(agent)
            print(f"  → CLASSIFIED AS SEVERE")
        else:
            # Test moderate condition
            moderate_condition_1 = total_errors >= moderate_threshold
            moderate_condition_2 = spam_error_count > 0 or email_error_count > 0
            is_moderate = moderate_condition_1 or moderate_condition_2

            print(f"  Moderate checks:")
            print(
                f"    total_errors >= moderate_threshold: {total_errors} >= {moderate_threshold} = {moderate_condition_1}"
            )
            print(
                f"    has any errors: {spam_error_count} > 0 OR {email_error_count} > 0 = {moderate_condition_2}"
            )
            print(
                f"    Overall moderate: {moderate_condition_1} OR {moderate_condition_2} = {is_moderate}"
            )

            if is_moderate:
                moderate_agents.append(agent)
                print(f"  → CLASSIFIED AS MODERATE")
            else:
                print(f"  → NOT CLASSIFIED (no errors)")

        print()

    print(f"RESULTS:")
    print(f"  Moderate agents: {len(moderate_agents)}")
    print(f"  Severe agents: {len(severe_agents)}")


if __name__ == "__main__":
    test_categorization()
