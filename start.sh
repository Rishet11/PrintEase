#!/bin/bash

# PrintEase Setup Script

echo "🖨️  PrintEase Setup"
echo "===================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your Razorpay credentials:"
    echo "   - RAZORPAY_KEY_ID"
    echo "   - RAZORPAY_KEY_SECRET"
    echo "   - SECRET_KEY (generate a random string)"
    echo ""
    read -p "Press Enter when you've updated .env..."
fi

# Activate virtual environment and run
echo ""
echo "🚀 Starting PrintEase server..."
source venv/bin/activate
python app.py
