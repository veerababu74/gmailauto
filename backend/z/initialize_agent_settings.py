#!/usr/bin/env python3
"""
Initialize Agent Settings Database with Sample Data
This script populates the database with default data for all agent settings.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.crud_connectivity_settings import connectivity_settings
from app.crud.crud_random_website_settings import random_website_settings
from app.crud.crud_default_sender import default_sender
from app.crud.crud_random_url import random_url


def initialize_connectivity_settings(db: Session):
    """Initialize connectivity settings with default values"""
    print("Initializing connectivity settings...")

    # Initialize default settings if they don't exist
    settings = connectivity_settings.initialize_default_settings(db)
    print(f"Created {len(settings)} connectivity settings")

    return settings


def initialize_random_website_settings(db: Session):
    """Initialize random website settings with default values"""
    print("Initializing random website settings...")

    # Initialize default settings if they don't exist
    settings = random_website_settings.initialize_default_settings(db)
    print(f"Created {len(settings)} random website settings")

    return settings


def initialize_default_senders(db: Session):
    """Initialize default senders with sample data"""
    print("Initializing default senders...")

    sample_senders = [
        {
            "email": "automation@gmail.com",
            "description": "Primary automation email sender",
            "is_active": True,
        },
        {
            "email": "noreply@company.com",
            "description": "Company notification sender",
            "is_active": True,
        },
        {
            "email": "marketing@company.com",
            "description": "Marketing campaign sender",
            "is_active": True,
        },
        {
            "email": "support@company.com",
            "description": "Customer support email sender",
            "is_active": True,
        },
        {
            "email": "notifications@app.com",
            "description": "Application notification sender",
            "is_active": False,
        },
    ]

    created_senders = []
    for sender_data in sample_senders:
        # Check if sender already exists
        existing = default_sender.get_by_email(db, sender_data["email"])
        if not existing:
            from app.schemas.default_sender import DefaultSenderCreate

            sender_create = DefaultSenderCreate(**sender_data)
            created_sender = default_sender.create(db, obj_in=sender_create)
            created_senders.append(created_sender)
            print(f"Created sender: {sender_data['email']}")
        else:
            print(f"Sender already exists: {sender_data['email']}")

    print(f"Created {len(created_senders)} new default senders")
    return created_senders


def initialize_random_urls(db: Session):
    """Initialize random URLs with sample data"""
    print("Initializing random URLs...")

    sample_urls = [
        {
            "url": "https://www.google.com",
            "category": "other",
            "description": "Google Search Engine",
            "is_active": True,
        },
        {
            "url": "https://www.facebook.com",
            "category": "social",
            "description": "Facebook Social Network",
            "is_active": True,
        },
        {
            "url": "https://www.instagram.com",
            "category": "social",
            "description": "Instagram Photo Sharing",
            "is_active": True,
        },
        {
            "url": "https://www.youtube.com",
            "category": "entertainment",
            "description": "YouTube Video Platform",
            "is_active": True,
        },
        {
            "url": "https://www.amazon.com",
            "category": "shopping",
            "description": "Amazon Online Shopping",
            "is_active": True,
        },
        {
            "url": "https://www.flipkart.com",
            "category": "shopping",
            "description": "Flipkart Online Shopping",
            "is_active": True,
        },
        {
            "url": "https://www.netflix.com",
            "category": "entertainment",
            "description": "Netflix Streaming Service",
            "is_active": True,
        },
        {
            "url": "https://www.linkedin.com",
            "category": "social",
            "description": "LinkedIn Professional Network",
            "is_active": True,
        },
        {
            "url": "https://www.twitter.com",
            "category": "social",
            "description": "Twitter Social Media",
            "is_active": True,
        },
        {
            "url": "https://www.reddit.com",
            "category": "social",
            "description": "Reddit Social News",
            "is_active": True,
        },
        {
            "url": "https://www.bbc.com",
            "category": "news",
            "description": "BBC News Website",
            "is_active": True,
        },
        {
            "url": "https://www.cnn.com",
            "category": "news",
            "description": "CNN News Network",
            "is_active": True,
        },
        {
            "url": "https://www.wikipedia.org",
            "category": "education",
            "description": "Wikipedia Encyclopedia",
            "is_active": True,
        },
        {
            "url": "https://www.github.com",
            "category": "technology",
            "description": "GitHub Code Repository",
            "is_active": True,
        },
        {
            "url": "https://www.stackoverflow.com",
            "category": "technology",
            "description": "Stack Overflow Programming Q&A",
            "is_active": True,
        },
        {
            "url": "https://www.spotify.com",
            "category": "entertainment",
            "description": "Spotify Music Streaming",
            "is_active": False,
        },
        {
            "url": "https://www.ebay.com",
            "category": "shopping",
            "description": "eBay Online Marketplace",
            "is_active": False,
        },
        {
            "url": "https://www.whatsapp.com",
            "category": "social",
            "description": "WhatsApp Messaging",
            "is_active": True,
        },
        {
            "url": "https://www.espn.com",
            "category": "sports",
            "description": "ESPN Sports News",
            "is_active": True,
        },
        {
            "url": "https://www.booking.com",
            "category": "travel",
            "description": "Booking.com Travel Site",
            "is_active": True,
        },
    ]

    created_urls = []
    for url_data in sample_urls:
        # Check if URL already exists
        existing = random_url.get_by_url(db, url_data["url"])
        if not existing:
            from app.schemas.random_url import RandomUrlCreate

            url_create = RandomUrlCreate(**url_data)
            created_url = random_url.create(db, obj_in=url_create)
            created_urls.append(created_url)
            print(f"Created URL: {url_data['url']} ({url_data['category']})")
        else:
            print(f"URL already exists: {url_data['url']}")

    print(f"Created {len(created_urls)} new random URLs")
    return created_urls


def main():
    """Main function to initialize all agent settings data"""
    print("Starting Agent Settings Database Initialization...")
    print("=" * 60)

    # Get database session
    db_generator = get_db()
    db = next(db_generator)

    try:
        # Initialize all settings
        connectivity_data = initialize_connectivity_settings(db)
        print()

        random_website_data = initialize_random_website_settings(db)
        print()

        default_sender_data = initialize_default_senders(db)
        print()

        random_url_data = initialize_random_urls(db)
        print()

        # Summary
        print("=" * 60)
        print("INITIALIZATION COMPLETE!")
        print(f"✅ Connectivity Settings: {len(connectivity_data)} items")
        print(f"✅ Random Website Settings: {len(random_website_data)} items")
        print(f"✅ Default Senders: {len(default_sender_data)} items")
        print(f"✅ Random URLs: {len(random_url_data)} items")
        print()
        print("Your Agent Settings page should now have data to display!")
        print("Navigate to: http://localhost:5173/agent-settings")

    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()
