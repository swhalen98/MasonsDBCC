#!/bin/bash
set -e

echo "========================================="
echo "Python version check:"
python --version
echo "========================================="

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt

# Initialize database
python database.py

echo "========================================="
echo "Build complete!"
echo "========================================="
