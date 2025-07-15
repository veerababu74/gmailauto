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

    # Get host and port from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    print(f"🚀 Starting Gmail Automation Dashboard API Server...")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print("-" * 50)

    # Simple uvicorn configuration for Render
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,
        access_log=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
