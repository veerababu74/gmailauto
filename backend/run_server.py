#!/usr/bin/env python3
"""
Production-ready server startup script for Gmail Automation Backend
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))


def start_server(
    host: str = None,
    port: int = None,
    reload: bool = False,
    workers: int = 1,
    production: bool = False,
):
    """
    Start the FastAPI server with proper configuration

    Args:
        host: Host to bind to (defaults to environment variable or 127.0.0.1)
        port: Port to listen on (defaults to environment variable or 8000)
        reload: Enable auto-reload for development
        workers: Number of worker processes (production only)
        production: Use production settings
    """

    # Use environment variables or defaults
    if host is None:
        host = os.getenv("HOST", "0.0.0.0" if production else "127.0.0.1")
    if port is None:
        port = int(os.getenv("PORT", "8000"))

    # Production settings
    if production:
        config = {
            "app": "app.main:app",
            "host": host,
            "port": port,
            "workers": workers,
            "loop": "uvloop",
            "http": "httptools",
            "access_log": True,
            "use_colors": False,
            "log_level": "info",
        }
    else:
        # Development settings
        config = {
            "app": "app.main:app",
            "host": host,
            "port": port,
            "reload": reload,
            "log_level": "debug",
            "access_log": True,
        }

    print(f"🚀 Starting Gmail Automation Dashboard API Server...")
    print(f"   Environment: {'Production' if production else 'Development'}")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    if production:
        print(f"   Workers: {workers}")
    print(f"   Reload: {reload}")
    print("-" * 60)

    try:
        uvicorn.run(**config)
    except KeyboardInterrupt:
        print("\n👋 Server shutdown requested by user")
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Gmail Automation Backend Server")
    parser.add_argument(
        "--host",
        default=None,
        help="Host to bind to (defaults to env var or 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to listen on (defaults to env var or 8000)",
    )
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--workers", type=int, default=1, help="Number of workers")
    parser.add_argument(
        "--production", action="store_true", help="Use production settings"
    )

    args = parser.parse_args()

    # Auto-detect production mode from environment
    if not args.production:
        args.production = (
            os.getenv("ENVIRONMENT", "development").lower() == "production"
        )

    # Validate environment
    if args.production and args.reload:
        print("❌ Cannot use --reload in production mode")
        sys.exit(1)

    start_server(
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers,
        production=args.production,
    )


if __name__ == "__main__":
    main()
