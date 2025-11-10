#!/bin/bash

# Deployment Script for Hostinger
# Run this script on your Hostinger server via SSH

echo "=========================================="
echo "Agnivridhi CRM - Hostinger Deployment"
echo "=========================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration - FOR SUBDOMAIN: crm.agnivridhiindia.com
PROJECT_DIR="/home/u623641178/public_html/crm.agnivridhiindia.com"
VENV_DIR="$PROJECT_DIR/venv"
PYTHON_VERSION="python3.9"  # Adjust based on Hostinger's Python version

echo -e "${YELLOW}Step 1: Checking Python version...${NC}"
$PYTHON_VERSION --version

echo ""
echo -e "${YELLOW}Step 2: Creating virtual environment...${NC}"
cd $PROJECT_DIR
$PYTHON_VERSION -m venv $VENV_DIR

echo ""
echo -e "${YELLOW}Step 3: Activating virtual environment...${NC}"
source $VENV_DIR/bin/activate

echo ""
echo -e "${YELLOW}Step 4: Upgrading pip...${NC}"
pip install --upgrade pip

echo ""
echo -e "${YELLOW}Step 5: Installing dependencies...${NC}"
pip install -r requirements-production.txt

echo ""
echo -e "${YELLOW}Step 6: Checking .env file...${NC}"
if [ -f "$PROJECT_DIR/.env" ]; then
    echo -e "${GREEN}.env file found!${NC}"
else
    echo -e "${RED}.env file NOT found! Please create it before continuing.${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 7: Running database migrations...${NC}"
python manage.py makemigrations
python manage.py migrate

echo ""
echo -e "${YELLOW}Step 8: Creating superuser (if needed)...${NC}"
echo "Do you want to create a superuser? (y/n)"
read -r create_superuser
if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

echo ""
echo -e "${YELLOW}Step 9: Collecting static files...${NC}"
python manage.py collectstatic --noinput

echo ""
echo -e "${YELLOW}Step 10: Setting permissions...${NC}"
chmod -R 755 $PROJECT_DIR
chmod 644 $PROJECT_DIR/.env
chmod 644 $PROJECT_DIR/passenger_wsgi.py
chmod 644 $PROJECT_DIR/.htaccess

echo ""
echo -e "${GREEN}=========================================="
echo "Deployment Complete!"
echo "==========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Ensure your domain is pointing to $PROJECT_DIR"
echo "2. Visit your domain to test the application"
echo "3. Login with your superuser credentials"
echo "4. Configure email settings if not done already"
echo ""
echo "Restart the application:"
echo "  mkdir -p tmp && touch tmp/restart.txt"
echo ""
