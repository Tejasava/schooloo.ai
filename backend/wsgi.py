"""
Vercel Serverless Functions Wrapper for Flask App
This file enables the Flask app to run on Vercel's serverless environment.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

# Import the Flask app
from app import app

# Vercel expects a WSGI application
# The app object from app.py is already a Flask instance (WSGI app)
