#!/bin/bash

# ================================================================
# PythonAnywhere Deployment Script for Agnivridhi CRM
# ================================================================
# Run this script in a PythonAnywhere Bash console after uploading your code
#
# BEFORE RUNNING:
# 1. Update USERNAME below with YOUR PythonAnywhere username
# 2. Create MySQL database in PythonAnywhere "Databases" tab
# 3. Upload .env.pythonanywhere as .env (or create it manually)
# ================================================================

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ================================================================
# CONFIGURATION - UPDATE THESE
# ================================================================
USERNAME="agnivridhi"  # <-- CHANGE THIS to your PythonAnywhere username
PROJECT_NAME="crm-agnivridhi"
PYTHON_VERSION="python3.10"
VENV_NAME="crm-env"

# Paths
PROJECT_DIR="/home/$USERNAME/$PROJECT_NAME"
VENV_PATH="/home/$USERNAME/.virtualenvs/$VENV_NAME"

echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}  Agnivridhi CRM - PythonAnywhere Deployment${NC}"
echo -e "${BLUE}================================================================${NC}"
echo ""

# ================================================================
# Step 1: Verify project directory
# ================================================================
echo -e "${YELLOW}Step 1: Verifying project directory...${NC}"
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}ERROR: Project directory not found: $PROJECT_DIR${NC}"
    echo "Please clone/upload your project first:"
    echo "  git clone https://github.com/Utkarsh1506/crm-agnivridhi.git $PROJECT_DIR"
    exit 1
fi
cd "$PROJECT_DIR"
echo -e "${GREEN}✓ Project directory found${NC}"
echo "  Location: $PROJECT_DIR"
echo ""

# ================================================================
# Step 2: Create virtual environment
# ================================================================
echo -e "${YELLOW}Step 2: Creating virtual environment...${NC}"
if [ ! -d "$VENV_PATH" ]; then
    mkvirtualenv --python=/usr/bin/$PYTHON_VERSION $VENV_NAME
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi
echo "  Path: $VENV_PATH"
echo ""

# ================================================================
# Step 3: Activate virtual environment
# ================================================================
echo -e "${YELLOW}Step 3: Activating virtual environment...${NC}"
source "$VENV_PATH/bin/activate"
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo "  Python version: $(python --version)"
echo ""

# ================================================================
# Step 4: Upgrade pip
# ================================================================
echo -e "${YELLOW}Step 4: Upgrading pip...${NC}"
python -m pip install --upgrade pip wheel setuptools
echo -e "${GREEN}✓ pip upgraded${NC}"
echo ""

# ================================================================
# Step 5: Install dependencies
# ================================================================
echo -e "${YELLOW}Step 5: Installing dependencies...${NC}"
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}ERROR: requirements.txt not found${NC}"
    exit 1
fi
echo ""

# ================================================================
# Step 6: Check .env file
# ================================================================
echo -e "${YELLOW}Step 6: Checking environment configuration...${NC}"
if [ ! -f "$PROJECT_DIR/.env" ]; then
    if [ -f "$PROJECT_DIR/.env.pythonanywhere" ]; then
        echo -e "${YELLOW}Found .env.pythonanywhere, copying to .env...${NC}"
        cp "$PROJECT_DIR/.env.pythonanywhere" "$PROJECT_DIR/.env"
        echo -e "${YELLOW}⚠ IMPORTANT: Edit .env and update these values:${NC}"
        echo "  1. SECRET_KEY (generate new one)"
        echo "  2. DB_PASSWORD (your MySQL password)"
        echo "  3. EMAIL_HOST_USER and EMAIL_HOST_PASSWORD"
        echo "  4. Replace 'agnivridhi' with '$USERNAME' in all paths"
        echo ""
        echo "Generate SECRET_KEY:"
        echo "  python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
        echo ""
        echo "After editing .env, run this script again."
        exit 0
    else
        echo -e "${RED}ERROR: .env file not found!${NC}"
        echo "Please create .env file with your configuration."
        echo "Use .env.pythonanywhere as a template."
        exit 1
    fi
fi

chmod 600 "$PROJECT_DIR/.env"
echo -e "${GREEN}✓ Environment file found and secured${NC}"
echo ""

# ================================================================
# Step 7: Database migrations
# ================================================================
echo -e "${YELLOW}Step 7: Running database migrations...${NC}"
python manage.py makemigrations
python manage.py migrate
echo -e "${GREEN}✓ Migrations complete${NC}"
echo ""

# ================================================================
# Step 8: Create superuser
# ================================================================
echo -e "${YELLOW}Step 8: Superuser creation${NC}"
echo -e "${YELLOW}Do you want to create a superuser? (y/n)${NC}"
read -r create_superuser
if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
    echo -e "${GREEN}✓ Superuser created${NC}"
else
    echo "Skipped superuser creation"
fi
echo ""

# ================================================================
# Step 9: Collect static files
# ================================================================
echo -e "${YELLOW}Step 9: Collecting static files...${NC}"
python manage.py collectstatic --noinput
echo -e "${GREEN}✓ Static files collected${NC}"
echo "  Location: $PROJECT_DIR/staticfiles"
echo ""

# ================================================================
# Step 10: Test configuration
# ================================================================
echo -e "${YELLOW}Step 10: Testing Django configuration...${NC}"
python manage.py check
echo -e "${GREEN}✓ Configuration valid${NC}"
echo ""

# ================================================================
# Deployment Complete
# ================================================================
echo -e "${GREEN}================================================================${NC}"
echo -e "${GREEN}  ✓ Deployment Complete!${NC}"
echo -e "${GREEN}================================================================${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Configure Web App in PythonAnywhere:"
echo "   → Go to: https://www.pythonanywhere.com/user/$USERNAME/webapps/"
echo "   → Click 'Add a new web app'"
echo "   → Choose 'Manual configuration' with Python 3.10"
echo ""
echo "2. Set these values in the Web tab:"
echo "   Source code:        $PROJECT_DIR"
echo "   Working directory:  $PROJECT_DIR"
echo "   Virtualenv:         $VENV_PATH"
echo ""
echo "3. Edit WSGI configuration file:"
echo "   → Update USERNAME to: $USERNAME"
echo "   → Copy contents from: pythonanywhere_wsgi.py"
echo ""
echo "4. Configure Static Files mapping:"
echo "   URL: /static/     Directory: $PROJECT_DIR/staticfiles"
echo "   URL: /media/      Directory: $PROJECT_DIR/media"
echo ""
echo "5. Reload your web app (big green button)"
echo ""
echo "6. Visit: https://$USERNAME.pythonanywhere.com"
echo ""
echo -e "${YELLOW}Troubleshooting:${NC}"
echo "   Error logs: Web tab → Log files → Error log"
echo "   Reload app: Web tab → Reload button"
echo ""
echo -e "${GREEN}Good luck! 🚀${NC}"
