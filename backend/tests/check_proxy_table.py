import sqlite3
import os

# Check if the database file exists
db_path = "data/gmail_dashboard.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if proxy_errors table exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='proxy_errors';"
    )
    result = cursor.fetchone()

    if result:
        print("✓ proxy_errors table exists in the database")

        # Get table schema
        cursor.execute("PRAGMA table_info(proxy_errors);")
        columns = cursor.fetchall()
        print("\nTable schema:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
    else:
        print("✗ proxy_errors table not found")

    conn.close()
else:
    print(f"✗ Database file not found at: {db_path}")
