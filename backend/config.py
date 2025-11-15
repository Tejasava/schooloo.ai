"""Configuration settings for Schooloo backend"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    
class ProductionConfig(Config):
    """Production configuration"""
    FLASK_ENV = 'production'

# Select config based on environment
config = DevelopmentConfig if os.getenv('FLASK_ENV') == 'development' else ProductionConfig
