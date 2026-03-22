"""
Configuration file for Schooloo backend and agent
Modify these settings as needed for your deployment
"""

# ============ BACKEND SETTINGS ============

BACKEND_HOST = '0.0.0.0'
BACKEND_PORT = 5000
DEBUG = True
TESTING = False

# ============ DATABASE SETTINGS ============

# Using in-memory database by default
# To use external database, modify database.py
DATABASE_TYPE = 'memory'  # Options: 'memory', 'sqlite', 'postgresql'
DATABASE_URL = 'sqlite:///schooloo.db'  # For SQLite
# DATABASE_URL = 'postgresql://user:password@localhost/schooloo'  # For PostgreSQL

# ============ AGENT SETTINGS ============

# Google API Configuration
GOOGLE_PROJECT_ID = 'your-project-id'
GOOGLE_API_KEY = 'your-google-api-key'  # For Gemini API

# Agent Model Configuration
AGENT_MODEL = 'gemini-pro'
AGENT_TEMPERATURE = 0.7
AGENT_MAX_TOKENS = 2048

# ============ SECURITY SETTINGS ============

# CORS Configuration
CORS_ORIGINS = ['*']  # Restrict in production: ['https://yourdomain.com']
CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

# Rate Limiting
RATE_LIMIT_ENABLED = False
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 60  # seconds

# Authentication (implement as needed)
API_KEY_REQUIRED = False
JWT_SECRET = 'your-secret-key'

# ============ LOGGING SETTINGS ============

LOG_LEVEL = 'INFO'
LOG_FILE = 'schooloo.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# ============ FEATURE FLAGS ============

FEATURES = {
    'lead_capture': True,
    'faq_management': True,
    'school_comparison': True,
    'nearby_schools': True,
    'exam_info': True,
    'document_tracking': True,
    'admin_dashboard': True,
}

# ============ SAMPLE DATA SETTINGS ============

# Load sample data on startup
LOAD_SAMPLE_DATA = True

# Sample schools to create
SAMPLE_SCHOOLS = [
    {
        'id': 'school_001',
        'name': 'Delhi Public School',
        'location': 'New Delhi, India',
        'latitude': 28.5355,
        'longitude': 77.2030,
    },
    {
        'id': 'school_002',
        'name': 'Greenfield Public School',
        'location': 'Bangalore, India',
        'latitude': 13.0827,
        'longitude': 77.6054,
    }
]

# ============ EMAIL SETTINGS (for notifications) ============

EMAIL_ENABLED = False
EMAIL_PROVIDER = 'smtp'  # Options: 'smtp', 'sendgrid', 'aws-ses'
EMAIL_FROM = 'noreply@schooloo.com'
SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your-email@gmail.com'
SMTP_PASSWORD = 'your-app-password'

# ============ SMS SETTINGS (for notifications) ============

SMS_ENABLED = False
SMS_PROVIDER = 'twilio'  # Options: 'twilio', 'aws-sns'
TWILIO_ACCOUNT_SID = 'your-twilio-sid'
TWILIO_AUTH_TOKEN = 'your-twilio-token'
TWILIO_PHONE_NUMBER = '+1234567890'

# ============ DEPLOYMENT SETTINGS ============

ENVIRONMENT = 'development'  # Options: 'development', 'staging', 'production'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# ============ API SETTINGS ============

API_VERSION = 'v1'
API_BASE_URL = '/api'
API_TIMEOUT = 30  # seconds

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# ============ CACHING SETTINGS ============

CACHE_ENABLED = False
CACHE_BACKEND = 'memory'  # Options: 'memory', 'redis'
CACHE_TTL = 3600  # seconds

# ============ ANALYTICS SETTINGS ============

ANALYTICS_ENABLED = False
ANALYTICS_PROVIDER = 'google'  # Options: 'google', 'mixpanel'
GOOGLE_ANALYTICS_ID = 'UA-XXXXXXXXX-X'

print("✅ Configuration loaded successfully")
