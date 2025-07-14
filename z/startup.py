#!/usr/bin/env python3
"""
Startup script for the FastAPI backend
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.init_db import init_db


def main():
    print("Initializing Gmail Automation Dashboard Backend...")

    # Create database tables
    print("Creating database tables...")
    init_db()

    print("Backend initialization complete!")
    print("You can now start the server with: uvicorn main:app --reload")


if __name__ == "__main__":
    main()
