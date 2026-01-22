# PrintEase - Shop Setup Guide

## Quick Setup (15 minutes)

### Step 1: Copy Files to Shop Computer

**Option A: USB Drive**
1. Copy entire `PrintEase` folder to USB
2. On shop computer, paste to Desktop or Documents

**Option B: GitHub** (if you have repository)
```bash
git clone https://github.com/yourusername/PrintEase.git
cd PrintEase
```

---

### Step 2: Install Python (If Not Installed)

**Windows:**
- Download from: https://www.python.org/downloads/
- ✅ Check "Add Python to PATH" during installation

**Mac:**
- Already installed, or use: `brew install python3`

**Linux:**
```bash
sudo apt install python3 python3-pip python3-venv
```

---

### Step 3: Setup Environment

Open Terminal/Command Prompt in PrintEase folder:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# Mac/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### Step 4: Configure Settings

Edit `.env` file (create from `.env.example`):

```bash
# Copy example file
cp .env.example .env

# Edit with their details
nano .env  # or use any text editor
```

**Required settings:**
```
UPI_ID=shopowner@paytm          # Shop's UPI ID
UPI_NAME=College Print Shop      # Shop name
STAFF_PIN=1234                   # Staff PIN (optional)
SECRET_KEY=random-secret-here    # Any random string
```

---

### Step 5: Setup Printer

**Set default printer in OS:**

**Windows:**
```
Settings → Devices → Printers → Right-click printer → Set as default
```

**Mac:**
```
System Settings → Printers & Scanners → Select printer → Set as default
```

**Linux:**
```bash
lpstat -p -d  # Check printers
lpoptions -d printer_name  # Set default
```

---

### Step 6: Start the Application

```bash
# Make sure venv is activated
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Run the app
python app.py
```

You'll see:
```
* Running on http://127.0.0.1:5001
* Running on http://192.168.x.x:5001  ← Share this IP
```

---

### Step 7: Share with Students

**Find the shop computer's IP:**

**Windows:**
```
ipconfig
# Look for "IPv4 Address" under WiFi
```

**Mac:**
```
ifconfig getifaddr en0
```

**Linux:**
```
hostname -I
```

**Students access:** `http://192.168.x.x:5001`

**Staff access:** `http://192.168.x.x:5001/staff`

---

## Auto-Start on Boot (Optional)

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Name: "PrintEase"
4. Trigger: "When computer starts"
5. Action: "Start a program"
6. Program: `C:\path\to\PrintEase\venv\Scripts\python.exe`
7. Arguments: `C:\path\to\PrintEase\app.py`
8. ✅ Finish

### Mac (LaunchAgent)

Create `~/Library/LaunchAgents/printease.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>printease</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/PrintEase/venv/bin/python</string>
        <string>/path/to/PrintEase/app.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Load: `launchctl load ~/Library/LaunchAgents/printease.plist`

### Linux (systemd)

Create `/etc/systemd/system/printease.service`:
```ini
[Unit]
Description=PrintEase Service
After=network.target

[Service]
User=shopuser
WorkingDirectory=/path/to/PrintEase
ExecStart=/path/to/PrintEase/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable printease
sudo systemctl start printease
```

---

## Testing Checklist

After setup, test these:

### Student Side:
- [ ] Access homepage from phone (`http://IP:5001`)
- [ ] Upload a test PDF
- [ ] Select print settings
- [ ] See UPI payment page
- [ ] Copy UPI ID works
- [ ] Click "I have paid"

### Staff Side:
- [ ] Access staff page (`http://IP:5001/staff`)
- [ ] Enter PIN (if set)
- [ ] See pending job
- [ ] Click "Approve & Print"
- [ ] Document prints from printer
- [ ] File auto-deletes

---

## Troubleshooting

### "Port 5001 already in use"
```bash
# Find and kill process
lsof -ti:5001 | xargs kill -9

# Or change port in .env
PORT=5002
```

### "Printer not found"
- Check printer is ON
- Check printer is set as default
- Test print from OS first

### "Can't access from phone"
- Check same WiFi network
- Check firewall allows port 5001
- Try disabling firewall temporarily

### "Permission denied" on files
```bash
chmod -R 755 PrintEase
```

---

## Files Structure

```
PrintEase/
├── .env              ← Configuration (MUST EDIT)
├── app.py            ← Main application
├── requirements.txt  ← Dependencies
├── jobs.json         ← Auto-created job queue
├── uploads/          ← Temporary PDF storage
├── venv/             ← Auto-created virtualenv
├── utils/            ← Helper functions
├── templates/        ← HTML pages
└── static/           ← CSS/JS files
```

---

## Daily Operation

**Morning:**
1. Turn on shop computer
2. App starts automatically (if configured)
3. OR manually run: `python app.py`

**Throughout Day:**
- Students upload → pay → staff approves → prints
- Check `jobs.json` if needed (job history)

**Evening:**
- Can leave running overnight
- OR stop with Ctrl+C

---

## Support

- System runs on: `http://localhost:5001`
- Students access: `http://[SHOP_IP]:5001`
- Staff access: `http://[SHOP_IP]:5001/staff`

**No internet required** - works on local WiFi only!
