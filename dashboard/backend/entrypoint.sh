#!/bin/bash
set -e

# Run the migrations
python migrate.py

# Load existing dashboard data
python load_data.py

# Start the Flask application
exec flask run --host=0.0.0.0 --port=5000