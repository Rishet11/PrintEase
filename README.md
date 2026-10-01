# PrintEase - Automated Print Service

PrintEase is a fully automated print service system that allows students to upload PDFs, pay via Razorpay, and get their documents printed automatically - no manual verification needed.

## Features

- **Instant Upload**: Upload PDF files up to 10MB
- **Flexible Print Settings**: Choose color mode, duplex, copies, orientation, and pages per sheet
- **Automated Payment**: Pay via UPI, cards, wallets, or net banking through Razorpay
- **Automatic Printing**: Documents print immediately after successful payment verification
- **Mobile-Friendly**: Works seamlessly on iOS and Android devices

## How It Works

1. **Student uploads PDF** and selects print settings
2. **System calculates total** based on settings and page count
3. **Razorpay checkout opens** for payment (UPI, GPay, PhonePe, Paytm, Cards)
4. **After successful payment**, signature is verified
5. **Document automatically prints** to the configured printer
6. **File is deleted** after printing for privacy

## Tech Stack

- **Backend**: Flask (Python)
- **Payment Gateway**: Razorpay
- **PDF Processing**: PyPDF2
- **OS-Level Printing**: System print commands

## Installation

### Prerequisites

- Python 3.11+
- A Razorpay account ([Sign up for test mode](https://dashboard.razorpay.com/signup))

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Rishet11/PrintEase.git
   cd PrintEase
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your Razorpay test credentials:
     ```
     RAZORPAY_KEY_ID=rzp_test_YOUR_KEY_ID
     RAZORPAY_KEY_SECRET=YOUR_KEY_SECRET
     SECRET_KEY=your-random-secret-key
     ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the app**:
   - Open browser to `http://localhost:5001`
   - On mobile (same network): `http://YOUR_COMPUTER_IP:5001`

## Getting Razorpay Test Keys

1. Go to [Razorpay Dashboard](https://dashboard.razorpay.com/)
2. Sign up or log in
3. Switch to **Test Mode** (toggle in top navigation)
4. Go to **Settings** → **API Keys**
5. Generate test keys
6. Copy Key ID and Key Secret to your `.env` file

## Testing Payments

In test mode, use these credentials:

**Test UPI**:
- UPI ID: `success@razorpay`

**Test Cards**:
- Card Number: `4111 1111 1111 1111`
- CVV: Any 3 digits
- Expiry: Any future date

## Pricing Configuration

Edit `config.py` to change prices:

```python
PRICE_BW_PER_PAGE = 2      # ₹2 per B&W page
PRICE_COLOR_PER_PAGE = 10  # ₹10 per color page
DUPLEX_DISCOUNT = 0.20     # 20% off for double-sided
```

## Deployment

**Recommended for Physical Printing:**
- **[Deploy with Cloudflare Tunnel](DEPLOY_CLOUDFLARE.md)** (Best reliability)
- **[Other Alternatives](DEPLOY_ALTERNATIVES.md)** (ngrok, zrok, Pinggy, etc.)

**Cloud Hosting (No Physical Printing):**
- [Deploy to Railway](DEPLOY_RAILWAY.md)
- [Deploy to Render](DEPLOY_RENDER.md)

## Security Notes

- Always use HTTPS in production
- Keep your Razorpay secret key secure
- Switch to live mode only after thorough testing
- Files are automatically deleted after printing

## License

MIT License. See [LICENSE](LICENSE) for the full text.

## Local Development

Run the Flask development server with:

```bash
python app.py
```

The application listens on port `5001` by default. Keep the `.env` file out of
version control and use Razorpay test credentials while developing.

## Troubleshooting

- If uploads fail, confirm the file is a PDF and is below the 10MB limit.
- If payments do not open, verify both Razorpay keys are present in `.env` and
  that the dashboard is in the same mode as the credentials.
- If printing fails, check that the target printer is available to the operating
  system and review the configured printer settings in `config.py`.
