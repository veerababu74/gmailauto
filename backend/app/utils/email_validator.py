#!/usr/bin/env python3
"""
Custom email validator to replace email-validator dependency
"""
import re
from typing import Any


class EmailValidationError(ValueError):
    """Custom exception for email validation errors"""

    pass


def validate_email(email: str) -> str:
    """
    Custom email validation function

    Args:
        email: Email string to validate

    Returns:
        str: Validated email string

    Raises:
        EmailValidationError: If email is invalid
    """
    if not isinstance(email, str):
        raise EmailValidationError("Email must be a string")

    # Basic email regex pattern
    # This covers most common email formats
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # Clean the email
    email = email.strip().lower()

    # Check if email matches the pattern
    if not re.match(email_pattern, email):
        raise EmailValidationError(f"Invalid email format: {email}")

    # Additional checks
    if len(email) > 254:  # RFC 5321 limit
        raise EmailValidationError("Email address too long")

    # Check for consecutive dots
    if ".." in email:
        raise EmailValidationError("Email contains consecutive dots")

    # Check for leading/trailing dots in local part
    local_part = email.split("@")[0]
    if local_part.startswith(".") or local_part.endswith("."):
        raise EmailValidationError("Email local part cannot start or end with dot")

    return email


def create_email_validator():
    """
    Create a Pydantic validator for email fields
    """

    def email_validator(cls, v: Any) -> str:
        if v is None:
            return v
        return validate_email(v)

    return email_validator


# Simple string type that will be validated by Pydantic validators
EmailStr = str


# Test function
def test_email_validator():
    """Test the email validator with various inputs"""
    test_cases = [
        ("user@example.com", True),
        ("test.email@domain.co.uk", True),
        ("user+tag@example.com", True),
        ("user123@example123.com", True),
        ("invalid.email", False),
        ("@example.com", False),
        ("user@", False),
        ("user..name@example.com", False),
        (".user@example.com", False),
        ("user.@example.com", False),
        ("", False),
        ("x" * 250 + "@example.com", False),
    ]

    print("🧪 Testing custom email validator:")
    for email, should_pass in test_cases:
        try:
            result = validate_email(email)
            if should_pass:
                print(f"✅ {email} -> {result}")
            else:
                print(f"❌ {email} should have failed but passed")
        except EmailValidationError as e:
            if not should_pass:
                print(f"✅ {email} -> Failed as expected: {e}")
            else:
                print(f"❌ {email} should have passed but failed: {e}")
        except Exception as e:
            print(f"❌ {email} -> Unexpected error: {e}")


if __name__ == "__main__":
    test_email_validator()
