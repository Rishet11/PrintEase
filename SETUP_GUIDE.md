# Setup Guide - PrintEase with Razorpay

This guide will help you set up PrintEase locally and configure it for automated payment processing with Razorpay.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Razorpay Configuration](#razorpay-configuration)
4. [Testing the Application](#testing-the-application)
5. [Printer Configuration](#printer-configuration)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Python 3.11 or higher**
  - Check version: `python3 --version`
  - Download: [python.org](https://www.python.org/downloads/)

- **Razorpay Account**
  - Sign up for free: [dashboard.razorpay.com/signup](https://dashboard.razorpay.com/signup)
  - Test mode available (no real money needed for testing)

### System Requirements

- macOS, Linux, or Windows
- A printer connected to your system (for actual printing)
- Network access (for Razorpay API)

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Rishet11/PrintEase.git
cd PrintEase
```

### 2. Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
ENVIRONMENT=development
RAZORPAY_KEY_ID=rzp_test_YOUR_KEY_ID
RAZORPAY_KEY_SECRET=YOUR_KEY_SECRET
SECRET_KEY=generate-a-random-secret-key
PORT=5001
```

**To generate a secret key:**

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## Razorpay Configuration

### 1. Get Test API Keys

1. Go to [Razorpay Dashboard](https://dashboard.razorpay.com/)
2. Sign up or log in
3. **Switch to Test Mode** (toggle in top-right corner)
4. Navigate to: **Settings** → **API Keys**
5. Click **Generate Test Key**
6. Copy both:
   - **Key ID** (starts with `rzp_test_`)
   - **Key Secret** (keep this private!)

### 2. Add Keys to .env File

```env
RAZORPAY_KEY_ID=rzp_test_ABC123XYZ
RAZORPAY_KEY_SECRET=your_secret_key_here
```

### 3. Enable Payment Methods

In Razorpay Dashboard (Test Mode):
- Go to **Settings** → **Payment Methods**
- Enable: UPI, Cards, Wallets, Net Banking
- All methods are enabled by default in test mode

---

## Testing the Application

### 1. Start the Application

```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5001
```

### 2. Access on Desktop

Open browser: `http://localhost:5001`

### 3. Access on Mobile (Same Network)

1. Find your computer's IP address:
   - **macOS**: `ifconfig | grep inet`
   - **Linux**: `ip addr show`
   - **Windows**: `ipconfig`

2. On mobile browser: `http://YOUR_IP_ADDRESS:5001`

### 4. Test Payment Flow

#### Razorpay Test Credentials

**UPI:**
- UPI ID: `success@razorpay` (for successful payment)
- UPI ID: `failure@razorpay` (for failed payment)

**Test Cards:**
- **Visa**: `4111 1111 1111 1111`
- **Mastercard**: `5555 5555 5555 4444`
- **CVV**: Any 3 digits
- **Expiry**: Any future date
- **Name**: Any name

**Test Wallets:**
- Select any wallet in the checkout
- Payment will automatically succeed

### 5. Complete Test Flow

1. Upload a PDF file
2. Select print settings (color, copies, etc.)
3. Click "Proceed to Payment"
4. Choose payment method (UPI/Card/Wallet)
5. Complete payment with test credentials
6. Verify document is sent to printer
7. Check that file is deleted from uploads folder

---

## Printer Configuration

### macOS/Linux

The app uses the system's default printer via `lp` command.

**Set default printer:**

```bash
# List available printers
lpstat -p -d

# Set default printer
lpoptions -d PRINTER_NAME
```

### Windows

The app uses Windows print command via PowerShell.

**Set default printer:**
1. Go to Settings → Devices → Printers & Scanners
2. Select your printer
3. Click "Manage" → "Set as default"

### Verify Printer Access

```bash
# macOS/Linux
lpstat -p -d

# Windows
Get-Printer | Select-Object Name, PrinterStatus
```

---

## Troubleshooting

### Issue: "RAZORPAY_KEY_ID must be set"

**Solution**: Ensure `.env` file exists and contains valid Razorpay keys.

```bash
# Verify .env file
cat .env
```

### Issue: Payment Not Working

**Checklist**:
1. Verify you're in **Test Mode** on Razorpay Dashboard
2. Check that API keys are correct in `.env`
3. Ensure no typos in key ID or secret
4. Restart the Flask app after changing `.env`

### Issue: Signature Verification Failed

**Solution**: Ensure you're using the correct key pair (Test or Live). Don't mix test and live keys.

### Issue: Printer Not Found

**macOS/Linux**:
```bash
# Check if CUPS is running
lpstat -r

# List printers
lpstat -p -d
```

**Windows**:
```powershell
# Check printer status
Get-Printer
```

### Issue: File Upload Fails

**Checklist**:
1. File size under 10MB
2. File is a valid PDF
3. `uploads/` folder exists and is writable

### Issue: Mobile Access Not Working

**Solution**:
1. Ensure computer and mobile are on same WiFi network
2. Check firewall settings allow incoming connections on port 5001
3. Use computer's local IP (not localhost) on mobile

**Temporarily disable firewall (testing only)**:

```bash
# macOS
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off

# Enable after testing
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
```

---

## Going to Production

When ready to accept real payments:

1. Switch Razorpay to **Live Mode**
2. Generate **Live API Keys**
3. Update `.env` with live keys
4. Set `ENVIRONMENT=production` in `.env`
5. Use HTTPS (required by Razorpay for live mode)
6. Deploy to a production server (see deployment guides)

---

## Support

For issues or questions:
- Check the [README](README.md)
- Review [Razorpay Documentation](https://razorpay.com/docs/)
- Open an issue on GitHub
