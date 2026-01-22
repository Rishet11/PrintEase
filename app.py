import os
import logging
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import config
from utils import file_handler, printer, job_queue, upi_generator

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

# Ensure folders exist
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    """Student upload portal."""
    return render_template('index.html')


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


@app.route('/create-job', methods=['POST'])
def create_job():
    """Create print job and show UPI payment."""
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
    
    # Create job
    job_id = job_queue.create_job(
        filepath=session['filepath'],
        filename=session['filename'],
        page_count=page_count,
        settings=settings,
        amount=total_price
    )
    
    # Clear session
    session.clear()
    
    return jsonify({
        'success': True,
        'job_id': job_id
    })


@app.route('/payment/<job_id>')
def payment_page(job_id):
    """Show UPI payment page."""
    job = job_queue.get_job(job_id)
    
    if not job:
        return "Job not found", 404
    
    # Generate UPI QR code
    qr_code = upi_generator.generate_upi_qr(
        upi_id=config.UPI_ID,
        amount=job['amount'],
        payee_name=config.UPI_NAME,
        transaction_note=f"PrintJob_{job_id}"
    )
    
    return render_template('payment_upi.html', 
                         job=job, 
                         qr_code=qr_code,
                         upi_id=config.UPI_ID,
                         config=config)


@app.route('/mark-paid/<job_id>', methods=['POST'])
def mark_paid(job_id):
    """Student marks payment as completed."""
    data = request.json
    utr = data.get('utr', '')
    
    job = job_queue.get_job(job_id)
    if not job:
        return jsonify({'success': False, 'error': 'Job not found'}), 404
    
    # Update UTR if provided
    if utr:
        jobs = job_queue._load_jobs()
        for j in jobs:
            if j['job_id'] == job_id:
                j['utr'] = utr
                job_queue._save_jobs(jobs)
                break
    
    return jsonify({
        'success': True,
        'message': 'Payment confirmation received. Please wait for staff approval.'
    })


@app.route('/staff')
def staff_page():
    """Staff verification page."""
    # Check if PIN is required
    if config.STAFF_PIN and not session.get('staff_authenticated'):
        return render_template('staff_login.html')
    
    # Get pending jobs
    pending_jobs = job_queue.get_pending_jobs()
    
    return render_template('staff.html', jobs=pending_jobs)


@app.route('/staff/login', methods=['POST'])
def staff_login():
    """Verify staff PIN."""
    if not config.STAFF_PIN:
        session['staff_authenticated'] = True
        return jsonify({'success': True})
    
    pin = request.json.get('pin', '')
    
    if pin == config.STAFF_PIN:
        session['staff_authenticated'] = True
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Invalid PIN'}), 401


@app.route('/staff/approve/<job_id>', methods=['POST'])
def approve_and_print(job_id):
    """Approve job and trigger printing."""
    # Check authentication
    if config.STAFF_PIN and not session.get('staff_authenticated'):
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    job = job_queue.get_job(job_id)
    if not job:
        return jsonify({'success': False, 'error': 'Job not found'}), 404
    
    # Mark as approved
    job_queue.approve_job(job_id)
    
    # Print document
    print_success, print_message = printer.print_document(job['filepath'], job['settings'])
    
    if print_success:
        # Mark as printed
        job_queue.mark_printed(job_id)
        
        # Delete file
        file_handler.delete_file(job['filepath'])
        
        return jsonify({
            'success': True,
            'message': 'Print job sent successfully'
        })
    else:
        return jsonify({
            'success': False,
            'error': f'Print failed: {print_message}'
        }), 500


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
