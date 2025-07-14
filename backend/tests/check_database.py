#!/usr/bin/env python3
"""
Check Agent Settings Database Data
This script shows what data is currently in the database.
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


def check_database_data():
    """Check what data exists in the database"""
    print("Checking Agent Settings Database Data...")
    print("=" * 60)

    # Get database session
    db_generator = get_db()
    db = next(db_generator)

    try:
        # Check connectivity settings
        print("🔗 CONNECTIVITY SETTINGS:")
        conn_settings = connectivity_settings.get_multi(db, limit=100)[0]
        print(f"   Total: {len(conn_settings)} items")
        for setting in conn_settings:
            print(
                f"   - {setting.setting_name}: {setting.setting_value} ({setting.setting_type})"
            )
        print()

        # Check random website settings
        print("🌐 RANDOM WEBSITE SETTINGS:")
        rw_settings = random_website_settings.get_multi(db, limit=100)[0]
        print(f"   Total: {len(rw_settings)} items")
        for setting in rw_settings:
            print(
                f"   - {setting.setting_name}: {setting.setting_value} ({setting.setting_type})"
            )
        print()

        # Check default senders
        print("📧 DEFAULT SENDERS:")
        senders = default_sender.get_multi(db, limit=100)[0]
        print(f"   Total: {len(senders)} items")
        for sender in senders:
            status = "✅" if sender.is_active else "❌"
            description = f" ({sender.description})" if sender.description else ""
            print(f"   {status} {sender.email}{description}")
        print()

        # Check random URLs
        print("🔗 RANDOM URLS:")
        urls = random_url.get_multi(db, limit=100)[0]
        print(f"   Total: {len(urls)} items")

        # Group by category
        categories = {}
        for url in urls:
            cat = url.category or "other"
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(url)

        for category, category_urls in categories.items():
            print(f"   📁 {category.upper()}: {len(category_urls)} items")
            for url in category_urls[:3]:  # Show first 3 items
                status = "✅" if url.is_active else "❌"
                print(f"      {status} {str(url.url)}")
            if len(category_urls) > 3:
                print(f"      ... and {len(category_urls) - 3} more")

        print()
        print("=" * 60)
        print("DATABASE CHECK COMPLETE!")

    except Exception as e:
        print(f"❌ Error checking database: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    check_database_data()
