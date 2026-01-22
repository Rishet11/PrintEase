# PrintEase - College Print Shop Automation

A simple Flask-based system for college print shops that eliminates queues through UPI payment verification and automatic printing.

## Features

✅ **Student Side**
- PDF upload (drag-and-drop, max 10MB)
- Print settings (color/B&W, duplex, copies, orientation, pages per sheet)
- UPI payment via QR code
- No account needed

✅ **Staff Side**
- Simple approval dashboard
- Manual payment verification
- One-click print approval
- Optional PIN protection

✅ **Auto-Print**
- Prints automatically after staff approval
- Supports macOS, Windows, Linux
- Auto-deletes files after printing

## Quick Start

### 1. Install

```bash
cd PrintEase
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
nano .env
```

Set your UPI details:
```
UPI_ID=yourshop@paytm
UPI_NAME=College Print Shop
STAFF_PIN=1234
SECRET_KEY=your-random-secret
```

### 3. Run

```bash
python app.py
```

Access at: `http://localhost:5001`

## How It Works

### Student Flow
1. Upload PDF
2. Select print settings
3. See UPI QR code + amount
4. Pay using any UPI app
5. Click "I have paid"
6. Wait for staff approval

### Staff Flow
1. Access `/staff` with PIN
2. See pending jobs
3. Verify payment in UPI app
4. Click "Approve & Print"
5. Document prints automatically

## Pricing

Configure in `config.py`:
- B&W: ₹2/page (default)
- Color: ₹10/page (default)
- Double-sided: 20% discount

## Local Network Access

Find your IP:
```bash
ipconfig getifaddr en0  # macOS
# Example: 192.168.1.100
```

Students access: `http://192.168.1.100:5001`

## Project Structure

```
PrintEase/
├── app.py              # Flask application
├── config.py           # Settings
├── jobs.json          # Job queue (auto-created)
├── requirements.txt    # Dependencies
├── utils/
│   ├── file_handler.py
│   ├── job_queue.py
│   ├── upi_generator.py
│   └── printer.py
├── templates/
│   ├── index.html
│   ├── payment_upi.html
│   ├── staff_login.html
│   └── staff.html
└── static/
    ├── css/style.css
    └── js/main.js
```

## Requirements

- Python 3.8+
- Configured default printer
- UPI account

## Why Manual UPI Instead of Razorpay?

✅ No API keys needed  
✅ No monthly fees  
✅ Works on local network  
✅ Direct printer access  
✅ Simple architecture  
✅ Staff has full control  

## License

Built for college print shops to reduce queues and manual file handling.
