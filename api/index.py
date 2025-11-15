"""
Vercel Serverless Function Handler for Schooloo API
Maps incoming requests to the Flask app handlers
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import Flask app
from app import app

# Export the Flask app for Vercel
def handler(request):
    """Vercel serverless handler that delegates to Flask"""
    # Vercel passes a Request object; Flask/WSGI expects environ dict
    # Use the WSGI app directly
    return app(request.environ, request.start_response)
