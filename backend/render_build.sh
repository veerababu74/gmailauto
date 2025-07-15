#!/bin/bash
# Render deployment build script - avoids Rust compilation issues
set -e

echo "🚀 Starting Render deployment build..."
echo "📍 Working directory: $(pwd)"
echo "🐍 Python version: $(python3 --version)"

# Upgrade pip first
echo "📦 Upgrading pip..."
python3 -m pip install --upgrade pip

# Install packages avoiding Rust compilation
echo "🔧 Installing dependencies (avoiding Rust compilation)..."
python3 -m pip install --no-cache-dir --only-binary=all \
  fastapi==0.104.1 \
  uvicorn==0.24.0 \
  gunicorn==21.2.0 \
  python-multipart==0.0.6 \
  python-jose==3.3.0 \
  passlib==1.7.4 \
  python-decouple==3.8 \
  sqlalchemy==2.0.23 \
  alembic==1.12.1 \
  pymysql==1.1.0 \
  mysql-connector-python==8.2.0 \
  aiosqlite==0.19.0 \
  pydantic==1.10.13 \
  email-validator==2.1.0 \
  httpx==0.25.2 \
  google-auth==2.23.4 \
  google-auth-oauthlib==1.1.0 \
  google-auth-httplib2==0.1.1 \
  google-api-python-client==2.108.0 \
  cryptography==3.4.8 \
  typing-extensions==4.8.0

echo "🗃️ Setting up database..."
python3 -c "
import os
import sys
sys.path.append('.')
try:
    from backend.database import init_db
    init_db()
    print('✅ Database initialized successfully')
except Exception as e:
    print(f'⚠️  Database initialization warning: {e}')
"

echo "✅ Build completed successfully!"
echo "🚀 Ready for deployment!"
