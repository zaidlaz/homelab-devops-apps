#!/bin/sh
# Entrypoint script for Docker container

# Create data and uploads directories if they don't exist
mkdir -p /app/data /app/uploads

# Initialize the database
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database initialized successfully!')
"

# Start gunicorn
exec gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile - --error-logfile - app:app
