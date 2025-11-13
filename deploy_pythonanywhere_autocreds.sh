#!/bin/bash
# PythonAnywhere Deployment Script
# Run these commands one by one in PythonAnywhere Bash Console

echo "=========================================="
echo "Deploying Auto-Credentials Feature"
echo "=========================================="
echo ""

# Step 1: Navigate to project
echo "Step 1: Navigate to project directory..."
cd ~/agnivridhi || cd ~/crm-agnivridhi || cd ~/CRM
pwd
echo ""

# Step 2: Pull latest code
echo "Step 2: Pulling latest code from GitHub..."
git pull origin main
echo ""

# Step 3: Activate virtual environment
echo "Step 3: Activating virtual environment..."
source venv/bin/activate || workon agnivridhi
echo ""

# Step 4: Run migrations
echo "Step 4: Running migrations..."
python manage.py makemigrations
python manage.py migrate
echo ""

# Step 5: Collect static files
echo "Step 5: Collecting static files..."
python manage.py collectstatic --noinput
echo ""

# Step 6: Test the feature
echo "Step 6: Running test script..."
python test_credential_generation.py
echo ""

echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Go to PythonAnywhere Web Tab"
echo "2. Click the RELOAD button"
echo "3. Visit your Owner Dashboard"
echo "4. Create a test client to see credentials"
echo ""
echo "Owner Dashboard URL:"
echo "https://your-username.pythonanywhere.com/dashboard/owner/"
echo ""
