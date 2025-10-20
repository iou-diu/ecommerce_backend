#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Wait for the database to be ready
echo "Waiting for the database to be ready..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "Database is ready!"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Make migrations
echo "Making migrations..."
python manage.py makemigrations

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:8085 --workers 3 --preload --log-level=debug --timeout 120
