import os
import logging
from flask import Flask, render_template, request, jsonify, session
import razorpay
import config
from utils import file_handler, printer

app = Flask(__name__)

# Production configuration
app.config.update(
    SESSION_COOKIE_SECURE=config.SESSION_COOKIE_SECURE,
    SESSION_COOKIE_HTTPONLY=config.SESSION_COOKIE_HTTPONLY,
    SESSION_COOKIE_SAMESITE=config.SESSION_COOKIE_SAMESITE
)

# Logging configuration
if config.IS_PRODUCTION:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )
else:
    logging.basicConfig(level=logging.DEBUG)

app.secret_key = config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE_MB * 1024 * 1024

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(config.RAZORPAY_KEY_ID, config.RAZORPAY_KEY_SECRET))

# Ensure folders exist
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    """Student upload portal."""
    return render_template('index.html', razorpay_key_id=config.RAZORPAY_KEY_ID)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle PDF upload and return pricing info."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Validate file
    is_valid, message = file_handler.validate_file(file)
    if not is_valid:
        return jsonify({'success': False, 'error': message}), 400
    
    # Save file
    filepath, filename = file_handler.save_file(file)
    
    # Get page count
    page_count = file_handler.get_page_count(filepath)
    if page_count == 0:
        file_handler.delete_file(filepath)
        return jsonify({'success': False, 'error': 'Could not read PDF'}), 400
    
    # Store in session
    session['filepath'] = filepath
    session['filename'] = filename
    session['page_count'] = page_count
    
    return jsonify({
        'success': True,
        'filename': filename,
        'page_count': page_count,
        'price_bw': config.PRICE_BW_PER_PAGE,
        'price_color': config.PRICE_COLOR_PER_PAGE
    })


@app.route('/create-order', methods=['POST'])
def create_order():
    """Create Razorpay order for payment."""
    if 'filepath' not in session:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
    
    data = request.json
    
    # Get settings
    settings = {
        'color_mode': data.get('color_mode', 'bw'),
        'duplex': data.get('duplex', 'single'),
        'copies': int(data.get('copies', 1)),
        'orientation': data.get('orientation', 'portrait'),
        'pages_per_sheet': int(data.get('pages_per_sheet', 1))
    }
    
    # Calculate price
    page_count = session.get('page_count', 1)
    total_price = file_handler.calculate_price(
        page_count, 
        settings['color_mode'], 
        settings['duplex'], 
        settings['copies']
    )
    
    # Store settings in session for later
    session['settings'] = settings
    session['amount'] = total_price
    
    try:
        # Create Razorpay order
        order_data = {
            'amount': int(total_price * 100),  # Convert to paise
            'currency': 'INR',
            'payment_capture': 1  # Auto-capture payment
        }
        
        razorpay_order = razorpay_client.order.create(data=order_data)
        
        return jsonify({
            'success': True,
            'order_id': razorpay_order['id'],
            'amount': total_price,
            'currency': 'INR'
        })
    
    except Exception as e:
        logging.error(f"Error creating Razorpay order: {e}")
        return jsonify({'success': False, 'error': 'Failed to create payment order'}), 500


@app.route('/verify-payment', methods=['POST'])
def verify_payment():
    """Verify Razorpay payment signature and trigger printing."""
    if 'filepath' not in session:
        return jsonify({'success': False, 'error': 'Session expired'}), 400
    
    data = request.json
    razorpay_order_id = data.get('razorpay_order_id')
    razorpay_payment_id = data.get('razorpay_payment_id')
    razorpay_signature = data.get('razorpay_signature')
    
    if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
        return jsonify({'success': False, 'error': 'Missing payment details'}), 400
    
    try:
        # Verify signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        razorpay_client.utility.verify_payment_signature(params_dict)
        
        # Signature verified - proceed with printing
        filepath = session.get('filepath')
        settings = session.get('settings')
        filename = session.get('filename')
        
        # Print document
        print_success, print_message = printer.print_document(filepath, settings)
        
        if print_success:
            # Delete file after successful print
            file_handler.delete_file(filepath)
            
            # Clear session
            session.clear()
            
            logging.info(f"Print job successful for {filename} - Payment ID: {razorpay_payment_id}")
            
            return jsonify({
                'success': True,
                'message': 'Payment verified! Your document is being printed.'
            })
        else:
            # Even if print fails, delete file and clear session
            file_handler.delete_file(filepath)
            session.clear()
            
            logging.error(f"Print failed for {filename}: {print_message}")
            return jsonify({
                'success': False,
                'error': f'Print failed: {print_message}'
            }), 500
    
    except razorpay.errors.SignatureVerificationError:
        # Invalid signature - delete file
        if 'filepath' in session:
            file_handler.delete_file(session['filepath'])
        session.clear()
        
        logging.warning(f"Invalid payment signature - Order: {razorpay_order_id}")
        return jsonify({'success': False, 'error': 'Payment verification failed'}), 400
    
    except Exception as e:
        # Any other error - cleanup
        if 'filepath' in session:
            file_handler.delete_file(session['filepath'])
        session.clear()
        
        logging.error(f"Error during payment verification: {e}")
        return jsonify({'success': False, 'error': 'Payment processing error'}), 500


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors."""
    logging.error(f"Internal error: {error}")
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'success': False, 'error': 'Not found'}), 404


if __name__ == '__main__':
    debug_mode = not config.IS_PRODUCTION
    app.run(debug=debug_mode, host='0.0.0.0', port=config.PORT)
