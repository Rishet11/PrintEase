import razorpay
import hmac
import hashlib
import config


def get_razorpay_client():
    """Get Razorpay client instance."""
    return razorpay.Client(auth=(config.RAZORPAY_KEY_ID, config.RAZORPAY_KEY_SECRET))


def create_order(amount_rupees):
    """Create Razorpay order. Amount in rupees, converted to paise."""
    client = get_razorpay_client()
    
    order_data = {
        'amount': amount_rupees * 100,  # Convert to paise
        'currency': 'INR',
        'payment_capture': 1  # Auto-capture payment
    }
    
    order = client.order.create(data=order_data)
    return order


def verify_payment(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    """Verify payment signature from Razorpay."""
    try:
        # Create signature verification string
        message = f"{razorpay_order_id}|{razorpay_payment_id}"
        
        # Generate expected signature
        expected_signature = hmac.new(
            config.RAZORPAY_KEY_SECRET.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures
        return hmac.compare_digest(expected_signature, razorpay_signature)
    except Exception:
        return False
