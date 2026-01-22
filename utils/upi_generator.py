import qrcode
import io
import base64


def generate_upi_qr(upi_id, amount, payee_name, transaction_note=''):
    """
    Generate UPI payment QR code.
    
    Args:
        upi_id: UPI ID (e.g., 'shop@upi')
        amount: Payment amount in rupees
        payee_name: Name of payee
        transaction_note: Optional transaction note
    
    Returns:
        Base64 encoded PNG image
    """
    # UPI payment URL format
    upi_url = f"upi://pay?pa={upi_id}&pn={payee_name}&am={amount}&cu=INR"
    
    if transaction_note:
        upi_url += f"&tn={transaction_note}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_base64}"
