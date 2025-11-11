#!/bin/bash

set -Eeuo pipefail
trap 'echo -e "\n\033[0;31m[ERROR] Failed at line $LINENO. See messages above.\033[0m"' ERR

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
PROJECT_DIR="/home/u623641178/domains/agnivridhiindia.com/public_html/crm.agnivridhiindia.com"
VENV_DIR="$PROJECT_DIR/venv"
PYTHON_VERSION="python3.9"  # Adjust based on Hostinger's Python version

echo -e "${YELLOW}Step 1: Checking Python version...${NC}"
if ! command -v "$PYTHON_VERSION" >/dev/null 2>&1; then
    echo -e "${RED}$PYTHON_VERSION not found. Trying python3...${NC}"
    PYTHON_VERSION="python3"
fi
"$PYTHON_VERSION" --version || { echo -e "${RED}No suitable Python found (tried python3.9 and python3).${NC}"; exit 1; }

echo ""
echo -e "${YELLOW}Step 2: Creating virtual environment...${NC}"
cd "$PROJECT_DIR"
echo "PWD: $(pwd)"
echo "Listing project directory (including hidden files):"
ls -la
"$PYTHON_VERSION" -m venv "$VENV_DIR"

echo ""
echo -e "${YELLOW}Step 3: Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

echo ""
echo -e "${YELLOW}Step 4: Upgrading pip...${NC}"
python -m pip install --upgrade pip wheel setuptools

echo ""
echo -e "${YELLOW}Step 5: Installing dependencies...${NC}"
REQ_FILE="$PROJECT_DIR/requirements-production.txt"
if [ ! -f "$REQ_FILE" ]; then
    echo -e "${YELLOW}requirements-production.txt not found, falling back to requirements.txt${NC}"
    REQ_FILE="$PROJECT_DIR/requirements.txt"
fi
pip install -r "$REQ_FILE"

echo ""
echo -e "${YELLOW}Step 6: Resolving environment file...${NC}"
ENV_FILE=""
for candidate in ".env" ".env.production" ".ENV" ".env.txt"; do
    if [ -f "$PROJECT_DIR/$candidate" ]; then
        ENV_FILE="$PROJECT_DIR/$candidate"
        break
    fi
done

if [ -z "${ENV_FILE}" ]; then
    echo -e "${RED}No environment file found in: $PROJECT_DIR${NC}"
    echo "Diagnostics:"
    echo "- Current directory: $(pwd)"
    echo "- Files present (hidden included):"
    ls -la "$PROJECT_DIR"
    echo "- Expected one of: .env, .env.production, .ENV, .env.txt"
    echo "Tip: If you uploaded from Windows, double-check the filename (no .txt extension) and location."
    exit 1
fi

ENV_BASENAME="$(basename "$ENV_FILE")"
if [ "$ENV_BASENAME" != ".env" ]; then
    echo -e "${YELLOW}Found $ENV_BASENAME. Copying to .env...${NC}"
    cp "$ENV_FILE" "$PROJECT_DIR/.env"
fi

# Normalize line endings to Unix to avoid potential parsing issues
if command -v sed >/dev/null 2>&1; then
    sed -i 's/\r$//' "$PROJECT_DIR/.env" || true
fi

chmod 600 "$PROJECT_DIR/.env"
echo -e "${GREEN}.env is ready.${NC}"

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
