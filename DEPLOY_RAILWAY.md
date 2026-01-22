# PrintEase Deployment - Railway

Railway is a simple deployment platform with automatic deployments from Git.

## Prerequisites
- GitHub account
- Railway account (sign up at railway.app)
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
# (You can do this via GitHub website)
git remote add origin https://github.com/YOUR_USERNAME/PrintEase.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Railway

1. **Sign in to Railway**: Go to [railway.app](https://railway.app)

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select the PrintEase repository

3. **Configure Environment Variables**:
   Go to project → Variables tab and add:
   ```
   ENVIRONMENT=production
   RAZORPAY_KEY_ID=rzp_live_xxxxx
   RAZORPAY_KEY_SECRET=your_secret_key
   SECRET_KEY=generate_random_string_here
   PORT=10000
   ```

4. **Deploy**:
   - Railway will automatically detect the Procfile
   - Click "Deploy"
   - Wait for deployment to complete

5. **Get Your URL**:
   - Railway will provide a URL like: `printease-production.up.railway.app`
   - Your app is now live!

### 3. Important Notes for Cloud Deployment

> [!WARNING]
> **Printer Limitation**: The cloud-deployed app CANNOT directly print to your local printer!

**Solution**: You need a "print server" running on the shop PC that polls for print jobs.

### Option A: Modified Architecture (Recommended)

Instead of direct printing, use a job queue:

1. **Cloud App**: Creates print jobs in a simple database
2. **Print Server** (shop PC): Polls database for new jobs and prints them

Would you like me to implement this architecture?

### Option B: Stick with Local Network

If you don't need remote access, local network deployment is simpler:
- No printer connectivity issues
- No monthly costs
- Easier to maintain

## Post-Deployment

### Test the Application
```bash
curl https://your-app.railway.app
```

### Monitor Logs
```bash
# In Railway dashboard, go to "Logs" tab
```

### Update Deployment
```bash
# Make changes, then push to GitHub
git add .
git commit -m "Update xyz"
git push

# Railway auto-deploys on push
```

## Costs

Railway Pricing:
- **Free Tier**: $5 credit/month (~100 hours)
- **Paid**: Pay as you go (~$5-10/month for light usage)

## Next Steps

Since cloud deployment can't print directly to your local printer, please choose:

**Option A**: Implement modified architecture with job queue
**Option B**: Switch to local network deployment

Which would you prefer?
