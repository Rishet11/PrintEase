import os
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename
import config


def allowed_file(filename):
    """Check if file has allowed extension (PDF only)."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def validate_file(file):
    """Validate uploaded file - check type and size."""
    if not file or file.filename == '':
        return False, "No file selected"
    
    if not allowed_file(file.filename):
        return False, "Only PDF files are allowed"
    
    # Check file size
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset to beginning
    
    max_size = config.MAX_FILE_SIZE_MB * 1024 * 1024
    if size > max_size:
        return False, f"File too large. Maximum size is {config.MAX_FILE_SIZE_MB}MB"
    
    return True, "Valid file"


def save_file(file):
    """Save uploaded file and return filepath."""
    filename = secure_filename(file.filename)
    # Add timestamp to avoid conflicts
    import time
    timestamp = int(time.time() * 1000)
    filename = f"{timestamp}_{filename}"
    
    filepath = os.path.join(config.UPLOAD_FOLDER, filename)
    file.save(filepath)
    return filepath, filename


def get_page_count(filepath):
    """Get number of pages in PDF."""
    try:
        reader = PdfReader(filepath)
        return len(reader.pages)
    except Exception:
        return 0


def delete_file(filepath):
    """Delete file after printing."""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    except Exception:
        pass
    return False


def calculate_price(page_count, color_mode, duplex, copies):
    """Calculate total price based on settings."""
    if color_mode == 'color':
        price_per_page = config.PRICE_COLOR_PER_PAGE
    else:
        price_per_page = config.PRICE_BW_PER_PAGE
    
    total = page_count * price_per_page * copies
    
    if duplex == 'double':
        total = total * (1 - config.DUPLEX_DISCOUNT)
    
    return int(total)  # Return as integer (paise will be handled separately)
