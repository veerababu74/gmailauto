#!/usr/bin/env python3
"""
Test the updated schemas with custom email validator
"""


def test_user_schema():
    try:
        from app.schemas.user import UserBase, UserCreate, User
        from app.utils.email_validator import EmailStr

        print("✅ User schema imports successful")

        # Test EmailStr validation
        valid_email = EmailStr("test@example.com")
        print(f"✅ Valid email: {valid_email}")

        # Test UserBase with valid email
        user_data = {"name": "Test User", "email": "test@example.com"}
        user = UserBase(**user_data)
        print(f"✅ UserBase creation successful: {user.email}")

        # Test invalid email
        try:
            user_data_invalid = {"name": "Test User", "email": "invalid.email"}
            invalid_user = UserBase(**user_data_invalid)
            print(f"❌ Should have failed: {invalid_user.email}")
        except Exception as e:
            print(f"✅ Invalid email rejected: {e}")

    except Exception as e:
        print(f"❌ User schema test failed: {e}")
        import traceback

        traceback.print_exc()


def test_default_sender_schema():
    try:
        from app.schemas.default_sender import DefaultSenderBase

        print("✅ Default sender schema imports successful")

        # Test with valid email
        sender_data = {"email": "sender@example.com"}
        sender = DefaultSenderBase(**sender_data)
        print(f"✅ DefaultSenderBase creation successful: {sender.email}")

    except Exception as e:
        print(f"❌ Default sender schema test failed: {e}")
        import traceback

        traceback.print_exc()


def test_main_import():
    try:
        from main import app

        print("✅ Main app imports successfully with custom email validator")
    except Exception as e:
        print(f"❌ Main app import failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    print("🧪 Testing schemas with custom email validator...")
    test_user_schema()
    print()
    test_default_sender_schema()
    print()
    test_main_import()
    print("\n🎯 Custom email validator test completed!")
