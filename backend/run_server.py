#!/usr/bin/env python3
"""
Simple server startup script for Gmail Automation Backend - Render Deployment
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))


def main():
    """Start the FastAPI server for Render deployment"""

    # Parse command line arguments
    import argparse

    parser = argparse.ArgumentParser(description="Gmail Automation Backend Server")
    parser.add_argument(
        "--production", action="store_true", help="Run in production mode"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of workers (currently ignored by uvicorn.run)",
    )
    args = parser.parse_args()

    # Get host and port from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    print(f"🚀 Starting Gmail Automation Dashboard API Server...")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Production Mode: {args.production}")
    print("-" * 50)

    # Configure uvicorn for production
    if args.production:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=False,
            access_log=True,
            log_level="info",
            workers=1,  # uvicorn.run doesn't support multiple workers, use gunicorn instead
        )
    else:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=True,
            access_log=True,
            log_level="debug",
        )


if __name__ == "__main__":
    main()
