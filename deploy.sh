#!/bin/bash
# Navigate to the backend directory and install dependencies
cd backend
pip install -r requirements.txt
# Use gunicorn to serve the Flask app (adjust the number of workers as necessary)
gunicorn -w 4 app:app