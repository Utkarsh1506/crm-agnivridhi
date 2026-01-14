#!/bin/bash
# Deploy reset changes to PythonAnywhere

cd ~/crm-agnivridhi
git fetch origin main
git reset --hard origin/main
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
touch /var/www/utkarsh1506_pythonanywhere_com_wsgi.py

echo "✅ PythonAnywhere updated to latest commit"
