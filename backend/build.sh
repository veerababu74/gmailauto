#!/bin/bash
# Build script for Render deployment
set -e

echo "Setting up Rust environment..."
export CARGO_HOME=/tmp/cargo
export RUSTUP_HOME=/tmp/rustup

# Create directories
mkdir -p /tmp/cargo
mkdir -p /tmp/rustup

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing Python dependencies..."
# Try main requirements first
if pip install --no-cache-dir -r requirements.txt; then
    echo "Main requirements installed successfully!"
else
    echo "Main requirements failed, trying fallback..."
    if pip install --no-cache-dir -r requirements-fallback.txt; then
        echo "Fallback requirements installed successfully!"
    else
        echo "Both requirement files failed. Trying without cache and with force reinstall..."
        pip install --upgrade --force-reinstall --no-cache-dir -r requirements.txt
    fi
fi

echo "Build completed successfully!"
