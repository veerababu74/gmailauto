#!/usr/bin/env python3
"""
Production startup script for Gmail Automation Backend on Render
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))


def setup_environment():
    """Setup environment for production"""

    print("🔧 Setting up production environment...")

    # Set production environment variables
    os.environ["ENVIRONMENT"] = "production"

    # Ensure required directories exist
    data_dir = backend_dir / "data"
    data_dir.mkdir(exist_ok=True)

    print("✅ Environment setup complete")


def run_database_migrations():
    """Run database migrations if needed"""

    print("🔄 Running database migrations...")

    try:
        # Import after setting up environment
        from app.db.init_db import init_db

        init_db()
        print("✅ Database initialization complete")

    except Exception as e:
        print(f"❌ Database migration failed: {e}")
        # Don't exit here - let the app handle DB creation
        print("ℹ️  Continuing with startup - app will handle DB creation")


def start_production_server():
    """Start the production server"""

    print("🚀 Starting production server...")

    # Get host and port from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "10000"))
    workers = int(os.getenv("WORKERS", "4"))

    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Workers: {workers}")

    # Start server using run_server.py
    try:
        from run_server import start_server

        start_server(
            host=host, port=port, production=True, workers=workers, reload=False
        )
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        sys.exit(1)


def main():
    """Main startup function"""

    print("🚀 Gmail Automation Backend - Production Startup")
    print("=" * 50)

    # Setup environment
    setup_environment()

    # Run database migrations
    run_database_migrations()

    # Start production server
    start_production_server()


if __name__ == "__main__":
    main()
