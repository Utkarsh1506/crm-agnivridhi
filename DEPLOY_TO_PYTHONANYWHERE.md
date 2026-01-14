# Deploy to PythonAnywhere

## SSH into PythonAnywhere and run:

```bash
# 1. Navigate to project directory
cd ~/crm-agnivridhi

# 2. Pull latest changes
git pull origin main

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install any new dependencies (if requirements.txt changed)
pip install -r requirements.txt

# 5. Run migrations (if any)
python manage.py migrate

# 6. Collect static files
python manage.py collectstatic --noinput

# 7. Reload web app
touch /var/www/utkarsh1506_pythonanywhere_com_wsgi.py
```

## Or use the Web tab:
1. Go to https://www.pythonanywhere.com/user/utkarsh1506/webapps/
2. Click "Reload" button

## Check if update successful:
- Visit your site: https://utkarsh1506.pythonanywhere.com
- Login and check dashboard
- Verify revenue data is showing correctly

## If errors occur:
- Check error logs in PythonAnywhere dashboard
- Look at: `/var/log/utkarsh1506.pythonanywhere.com.error.log`
