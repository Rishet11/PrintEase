# Deploy with Cloudflare Tunnel (Recommended)

This is the **BEST** deployment method for PrintEase because:
1.  **Public Access**: Students can access the site from anywhere (4G/5G/WiFi).
2.  **Local Printing**: The code runs on *your* computer, so it can still send commands to your physical USB printer.
3.  **Secure**: No need to open router ports or expose your IP address.
4.  **Free**: Cloudflare Tunnel is completely free.

---

## 🚀 Quick Setup (Temporary)

Use this method to test quickly or if you only run the shop for a few hours.

### 1. Install Cloudflare Tunnel

**macOS (Homebrew):**
```bash
brew install cloudflare/cloudflared
```

**Windows:**
1. Download `cloudflared` from [Cloudflare Downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/).
2. Rename the file to `cloudflared.exe`.
3. Open PowerShell in that folder.

### 2. Start the App
Make sure your Flask app is running in one terminal:
```bash
python app.py
```
*(It should be running on port 5001)*

### 3. Start the Tunnel
Open a **new terminal** window and run:

```bash
cloudflared tunnel --url http://localhost:5001
```

### 4. Get the Link
Look for a line in the output that says:
`+--------------------------------------------------------------------------------------------+`
`|  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |`
`|  https://random-name-xyz.trycloudflare.com                                                 |`
`+--------------------------------------------------------------------------------------------+`

**Copy that https link**. This is your public website URL!
Generate a QR code for this link and stick it on your shop wall.

---

## 🔒 Permanent Setup (Custom Domain)

If you have a domain name (e.g., `myprintshop.com`) connected to Cloudflare, you can set up a permanent stable link.

1.  **Login to Cloudflare**:
    ```bash
    cloudflared tunnel login
    ```
    (This will open a browser window to authorize).

2.  **Create a Tunnel**:
    ```bash
    cloudflared tunnel create printshop
    ```

3.  **Configure the Tunnel**:
    Create a file named `config.yml` in `~/.cloudflared/` folder:
    ```yaml
    tunnel: <Tunnel-UUID-from-step-2>
    credentials-file: /Users/yourname/.cloudflared/<Tunnel-UUID>.json

    ingress:
      - hostname: print.myprintshop.com
        service: http://localhost:5001
      - service: http_status:404
    ```

4.  **Route DNS**:
    ```bash
    cloudflared tunnel route dns printshop print.myprintshop.com
    ```

5.  **Run the Tunnel**:
    ```bash
    cloudflared tunnel run printshop
    ```

Now `print.myprintshop.com` will always point to your laptop, as long as the tunnel is running!
