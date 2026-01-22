import os
from dotenv import load_dotenv

load_dotenv()

# Environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
IS_PRODUCTION = ENVIRONMENT == 'production'

# Flask Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
if IS_PRODUCTION and SECRET_KEY == 'dev-secret-key-change-in-production':
    raise ValueError("SECRET_KEY must be set in production!")

# Session Configuration (secure in production)
SESSION_COOKIE_SECURE = IS_PRODUCTION  # HTTPS only in production
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# UPI Configuration
UPI_ID = os.getenv('UPI_ID', 'printshop@upi')
UPI_NAME = os.getenv('UPI_NAME', 'College Print Shop')

# Staff Access (optional PIN)
STAFF_PIN = os.getenv('STAFF_PIN', '')  # Leave empty to disable PIN

# File Upload Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {'pdf'}

# Job Queue Storage
JOBS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jobs.json')

# Pricing Configuration (in Rupees)
PRICE_BW_PER_PAGE = 2
PRICE_COLOR_PER_PAGE = 10
DUPLEX_DISCOUNT = 0.20  # 20% discount for double-sided

# Server Configuration
PORT = int(os.getenv('PORT', 5001))
HOST = '0.0.0.0' if IS_PRODUCTION else '127.0.0.1'
