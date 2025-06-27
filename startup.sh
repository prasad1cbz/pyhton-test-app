#!/bin/bash

# Production startup script for Python Web App
echo "🚀 Starting Python Web App..."

# Set environment variables
export FLASK_ENV=production
export FLASK_DEBUG=False
export PORT=${PORT:-8000}
export HOST=${HOST:-0.0.0.0}

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Start the application with gunicorn for production
echo "🌐 Starting application on $HOST:$PORT"
exec gunicorn --bind $HOST:$PORT --workers 4 --timeout 120 --access-logfile - --error-logfile - main:app 