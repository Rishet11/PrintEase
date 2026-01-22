# PrintEase Deployment - Render

Render offers free tier hosting with automatic deployments from Git.

## Prerequisites
- GitHub account
- Render account (sign up at render.com)
- Razorpay LIVE API keys

## Deployment Steps

### 1. Prepare Repository
```bash
cd /Users/rishetmehra/Desktop/PrintEase

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit - PrintEase v1.0"

# Create GitHub repository and push
git remote add origin https://github.com/YOUR_USERNAME/PrintEase.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Render

1. **Sign in to Render**: Go to [render.com](https://render.com)

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select the PrintEase repository

3. **Configure Service**:
   - **Name**: printease
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app --bind 0.0.0.0:$PORT`

4. **Environment Variables**:
   Add these in the "Environment" section:
   ```
   ENVIRONMENT=production
   RAZORPAY_KEY_ID=rzp_live_xxxxx
   RAZORPAY_KEY_SECRET=your_secret_key
   SECRET_KEY=generate_random_string_here
   ```

5. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes first time)

6. **Get Your URL**:
   - Render provides: `printease.onrender.com`

### 3. Important Printer Connectivity Issue

> [!CAUTION]
> **Critical Limitation**: Cloud-hosted apps CANNOT print to local printers!

The cloud server is in a data center, not connected to your shop printer.

### Solutions:

**Option A: Hybrid Architecture** (Cloud + Local Print Server)
```
Student → Cloud App (Railway/Render) → Database
                                          ↓
                      Shop PC ← Print Server ← Polls for jobs
                         ↓
                     Printer
```

**Option B: Local Network Only**
- Run Flask on shop PC
- Access via WiFi only
- Direct printing works
- No monthly costs

## Which Should You Choose?

| Feature | Cloud | Local Network |
|---------|-------|---------------|
| Remote access | ✅ Yes | ❌ No (WiFi only) |
| Direct printing | ❌ No | ✅ Yes |
| Monthly cost | ~$5-10 | Free |
| Setup complexity | Medium | Easy |
| Maintenance | Low | Low |

## Render Free Tier

- ✅ Free tier available
- ⚠️ Spins down after 15 min inactivity (cold starts ~30s)
- ⚠️ 750 hours/month limit

## Recommendation

For a **college print shop**, I recommend:
1. **Local network deployment** (simplest, works perfectly)
2. If you really need remote access, use hybrid architecture

Would you like to proceed with local network deployment instead?
