#!/bin/bash
# Emergency deployment script for Python 3.13 compatibility
set -e

echo "🚨 Emergency deployment for Python 3.13 compatibility"
echo "🐍 Current Python version: $(python3 --version)"

# Force Python 3.12 if possible
if command -v python3.12 &> /dev/null; then
    echo "✅ Found Python 3.12, using it"
    PYTHON_CMD="python3.12"
else
    echo "⚠️  Python 3.12 not found, using default python3"
    PYTHON_CMD="python3"
fi

# Upgrade pip
echo "📦 Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip

# Install with specific versions for Python 3.13
echo "🔧 Installing Python 3.13 compatible packages..."
$PYTHON_CMD -m pip install --no-cache-dir \
  fastapi==0.104.1 \
  uvicorn==0.35.0 \
  gunicorn==21.2.0 \
  python-multipart==0.0.6 \
  python-jose==3.3.0 \
  passlib==1.7.4 \
  python-decouple==3.8 \
  sqlalchemy==2.0.35 \
  alembic==1.13.1 \
  pymysql==1.1.1 \
  mysql-connector-python==9.3.0 \
  aiosqlite==0.19.0 \
  pydantic==1.10.17 \
  email-validator==2.1.0 \
  httpx==0.25.2 \
  google-auth==2.23.4 \
  google-auth-oauthlib==1.1.0 \
  google-auth-httplib2==0.1.1 \
  google-api-python-client==1.6.3 \
  cryptography==41.0.7 \
  typing-extensions==4.13.2

echo "✅ Emergency deployment packages installed"
echo "🎯 Ready for deployment"
