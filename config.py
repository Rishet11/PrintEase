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

# Razorpay Configuration
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')

if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
    raise ValueError("RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET must be set!")

# File Upload Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {'pdf'}

# Pricing Configuration (in Rupees)
PRICE_BW_PER_PAGE = 2
PRICE_COLOR_PER_PAGE = 10
DUPLEX_DISCOUNT = 0.20  # 20% discount for double-sided

# Server Configuration
PORT = int(os.getenv('PORT', 5001))
HOST = '0.0.0.0' if IS_PRODUCTION else '127.0.0.1'
