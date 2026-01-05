#!/bin/bash
# ============================================================================
# Quick Setup Script for PythonAnywhere - Copy-Paste Ready
# ============================================================================
# This script will:
# 1. Pull latest code from GitHub
# 2. Regenerate all barcodes with correct domain
# 3. Reload the web app
#
# Usage: Paste entire script into PythonAnywhere Bash Console
# ============================================================================

echo "=========================================="
echo "🚀 Agnivridhi CRM - PythonAnywhere Setup"
echo "=========================================="

# Replace with YOUR actual username
USERNAME="agnivridhicrm"

# Paths
PROJECT_DIR="/home/$USERNAME/crm-agnivridhi"
VENV_DIR="/home/$USERNAME/.virtualenvs/agnivridhicrm38"  # Adjust venv name if needed
WSGI_FILE="/var/www/${USERNAME}_pythonanywhere_com_wsgi.py"

echo ""
echo "Step 1: Navigate to project..."
cd "$PROJECT_DIR" || { echo "❌ Failed to cd to $PROJECT_DIR"; exit 1; }
echo "✓ In: $(pwd)"

echo ""
echo "Step 2: Pull latest code from GitHub..."
git pull origin main
if [ $? -ne 0 ]; then
  echo "❌ Git pull failed!"
  exit 1
fi
echo "✓ Code pulled"

echo ""
echo "Step 3: Activate virtual environment..."
source "$VENV_DIR/bin/activate" || { echo "❌ Failed to activate venv"; exit 1; }
echo "✓ Venv activated: $VIRTUAL_ENV"

echo ""
echo "Step 4: Install dependencies (if needed)..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

echo ""
echo "Step 5: Run database migrations..."
python manage.py migrate employees
if [ $? -ne 0 ]; then
  echo "❌ Migrations failed!"
  exit 1
fi
echo "✓ Migrations done"

echo ""
echo "Step 6: Regenerate ALL barcodes with verification URLs..."
python manage.py generate_employee_barcodes --force
if [ $? -ne 0 ]; then
  echo "❌ Barcode generation failed!"
  exit 1
fi
echo "✓ All barcodes regenerated"

echo ""
echo "Step 7: Reload web app..."
touch "$WSGI_FILE"
echo "✓ Web app reloaded"

echo ""
echo "=========================================="
echo "✅ SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Open browser: https://agnivridhicrm.pythonanywhere.com/employees/verify/0101/"
echo "2. You should see employee details WITHOUT login"
echo "3. Scan a barcode - it should open the verification page"
echo ""
