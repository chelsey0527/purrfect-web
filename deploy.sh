#!/bin/bash
# Navigate to the backend directory and install dependencies
cd backend
pip install -r requirements.txt
# Use gunicorn to serve the Flask app (adjust the number of workers as necessary)
gunicorn --bind=0.0.0.0:8080 -w 4 app:app