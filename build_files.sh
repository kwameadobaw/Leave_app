#!/bin/bash

# Exit on error
set -e

echo "Creating virtual environment..."
python -m venv venv

# Detect OS and use appropriate activation command
if [ "$VERCEL" = "1" ]; then
    echo "Activating virtual environment on Vercel..."
    source venv/bin/activate
else
    # For local Windows testing, this won't actually run but is here for reference
    echo "For Windows, activate with: venv\Scripts\activate"
    source venv/bin/activate 2>/dev/null || true
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!"