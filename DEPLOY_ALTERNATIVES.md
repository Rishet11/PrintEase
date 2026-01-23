# Alternative Deployment Options

If you don't want to use Cloudflare Tunnel, here are the best free alternatives to expose your local PrintEase app to the internet.

## 1. zrok (Best Open Source Alternative)

**zrok** is an open-source sharing platform that is completely free and very generous.

**Pros:**
- Open source & free
- **Persistent public URLs** (even on free tier!)
- faster than ngrok in many cases

**Setup:**
1. Install zrok: `brew install zrok` (macOS)
2. Invite yourself: `zrok invite`
3. Enable your environment (follow email instructions)
4. Share your app:
   ```bash
   zrok share public http://localhost:5001 --headless
   ```

---

## 2. ngrok (Most Popular)

**ngrok** is the industry standard, but the free plan has limits.

**Pros:**
- Extremely reliable
- Easy to set up

**Cons:**
- **Random URL every time** you restart (on free plan)
- Session time limits sometimes apply

**Setup:**
1. Sign up at [ngrok.com](https://ngrok.com)
2. Install: `brew install ngrok/ngrok/ngrok`
3. Connect account: `ngrok config add-authtoken <TOKEN>`
4. Run:
   ```bash
   ngrok http 5001
   ```

---

## 3. localhost.run (No Installation Required)

Uses SSH, so you don't need to install any new software.

**Pros:**
- Zero installation
- Instant setup

**Setup:**
Run this command in terminal:
```bash
ssh -R 80:localhost:5001 nokey@localhost.run
```
It will print a URL for you to use.

---

## 4. Pinggy (easiest with persistent URL option)

**Pinggy** gives you a public URL with a single command, and provides a nice terminal UI.

**Setup:**
```bash
ssh -p 443 -R0:localhost:5001 qr@a.pinggy.io
```
**Bonus:** This command automatically generates a **QR Code** in your terminal!

---

## Summary Comparison

| Service | Price | Static URL? | Installation? | Best For... |
| :--- | :--- | :--- | :--- | :--- |
| **Cloudflare** | Free | Yes (requires domain) | Yes | **Production / Stability** |
| **zrok** | Free | **Yes** (Free) | Yes | **Best Free All-Rounder** |
| **ngrok** | Freemium | No (Free tier) | Yes | Quick Testing |
| **Pinggy** | Free | No | **No** | **Instant QR Code** |
