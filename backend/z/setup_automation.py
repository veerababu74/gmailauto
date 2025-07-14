"""
Startup script for Gmail Automation Backend
Initializes database and default settings
"""

from sqlalchemy import create_engine
from app.core.config import settings
from app.core.database import SessionLocal
from app.db.init_db import init_db
from app.crud.crud_default_sender import default_sender
from app.crud.crud_random_url import random_url
from app.crud.crud_random_website_settings import random_website_settings
from app.crud.crud_connectivity_settings import connectivity_settings
from app.schemas.default_sender import DefaultSenderCreate
from app.schemas.random_url import RandomUrlCreate


def initialize_default_data():
    """Initialize default data for automation settings"""

    db = SessionLocal()
    try:
        print("Initializing default automation settings...")

        # Initialize random website settings
        print("Setting up random website settings...")
        random_website_settings.initialize_default_settings(db)

        # Initialize connectivity settings
        print("Setting up connectivity settings...")
        connectivity_settings.initialize_default_settings(db)

        # Initialize default URLs if none exist
        if not random_url.get_active(db):
            print("Setting up default random URLs...")
            default_urls = [
                {
                    "url": "https://www.instagram.com",
                    "category": "social",
                    "description": "Instagram",
                },
                {
                    "url": "https://www.facebook.com",
                    "category": "social",
                    "description": "Facebook",
                },
                {
                    "url": "https://www.youtube.com",
                    "category": "entertainment",
                    "description": "YouTube",
                },
                {
                    "url": "https://www.flipkart.com",
                    "category": "shopping",
                    "description": "Flipkart",
                },
                {
                    "url": "https://www.amazon.in",
                    "category": "shopping",
                    "description": "Amazon India",
                },
                {
                    "url": "https://www.indiatimes.com",
                    "category": "news",
                    "description": "Times of India",
                },
                {
                    "url": "https://www.ndtv.com",
                    "category": "news",
                    "description": "NDTV",
                },
                {
                    "url": "https://www.cricbuzz.com",
                    "category": "sports",
                    "description": "Cricbuzz",
                },
                {
                    "url": "https://www.hotstar.com",
                    "category": "entertainment",
                    "description": "Hotstar",
                },
                {
                    "url": "https://www.zomato.com",
                    "category": "other",
                    "description": "Zomato",
                },
                {
                    "url": "https://www.irctc.co.in",
                    "category": "travel",
                    "description": "IRCTC",
                },
                {
                    "url": "https://www.myntra.com",
                    "category": "shopping",
                    "description": "Myntra",
                },
                {
                    "url": "https://www.ajio.com",
                    "category": "shopping",
                    "description": "Ajio",
                },
                {
                    "url": "https://www.snapdeal.com",
                    "category": "shopping",
                    "description": "Snapdeal",
                },
                {
                    "url": "https://www.paytm.com",
                    "category": "finance",
                    "description": "Paytm",
                },
                {
                    "url": "https://www.swiggy.com",
                    "category": "other",
                    "description": "Swiggy",
                },
                {
                    "url": "https://www.ola.com",
                    "category": "travel",
                    "description": "Ola",
                },
                {
                    "url": "https://www.makemytrip.com",
                    "category": "travel",
                    "description": "MakeMyTrip",
                },
                {
                    "url": "https://www.quora.com",
                    "category": "social",
                    "description": "Quora",
                },
                {
                    "url": "https://www.linkedin.com",
                    "category": "social",
                    "description": "LinkedIn",
                },
                {
                    "url": "https://www.twitter.com",
                    "category": "social",
                    "description": "Twitter",
                },
                {
                    "url": "https://www.reddit.com",
                    "category": "social",
                    "description": "Reddit",
                },
                {
                    "url": "https://www.medium.com",
                    "category": "education",
                    "description": "Medium",
                },
                {
                    "url": "https://www.github.com",
                    "category": "technology",
                    "description": "GitHub",
                },
                {
                    "url": "https://www.stackoverflow.com",
                    "category": "technology",
                    "description": "Stack Overflow",
                },
                {
                    "url": "https://www.wikipedia.org",
                    "category": "education",
                    "description": "Wikipedia",
                },
                {
                    "url": "https://www.bbc.com",
                    "category": "news",
                    "description": "BBC",
                },
                {
                    "url": "https://www.cnn.com",
                    "category": "news",
                    "description": "CNN",
                },
                {
                    "url": "https://www.nytimes.com",
                    "category": "news",
                    "description": "New York Times",
                },
                {
                    "url": "https://www.theguardian.com",
                    "category": "news",
                    "description": "The Guardian",
                },
            ]

            for url_data in default_urls:
                url_create = RandomUrlCreate(**url_data)
                random_url.create(db, obj_in=url_create)

            print(f"Created {len(default_urls)} default random URLs")

        # Initialize default sender if none exist
        if not default_sender.get_active(db):
            print("Setting up default sender...")
            default_email = DefaultSenderCreate(
                email="info@findexco.com",
                description="Default sender email for automation",
                is_active=True,
            )
            default_sender.create(db, obj_in=default_email)
            print("Created default sender: info@findexco.com")

        print("✅ Default automation settings initialized successfully!")

    except Exception as e:
        print(f"❌ Error initializing default data: {e}")
        raise
    finally:
        db.close()


def main():
    """Main startup function"""
    print("🚀 Starting Gmail Automation Backend...")

    # Initialize database tables
    print("📁 Initializing database tables...")
    init_db()

    # Initialize default data
    initialize_default_data()

    print("✅ Backend startup completed successfully!")
    print("\n📋 Available API endpoints:")
    print("  - Default Senders: /api/v1/default-senders")
    print("  - Random URLs: /api/v1/random-urls")
    print("  - Random Website Settings: /api/v1/random-website-settings")
    print("  - Connectivity Settings: /api/v1/connectivity-settings")
    print("  - Complete Automation Config: /api/v1/automation/automation-config")
    print("\n🌐 API Documentation: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
