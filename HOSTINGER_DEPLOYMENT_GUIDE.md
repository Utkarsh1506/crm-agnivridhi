# Hostinger Deployment Guide - Agnivridhi CRM

## 📋 Prerequisites

Before deploying to Hostinger, ensure you have:
- ✅ Hostinger hosting account with Python support
- ✅ MySQL database access via phpMyAdmin
- ✅ SSH access to your Hostinger server
- ✅ Domain name configured (optional but recommended)
- ✅ Your CRM code ready for deployment

---

## 🗄️ Step 1: Create MySQL Database on Hostinger

### Via phpMyAdmin:

1. **Login to Hostinger Control Panel**
   - Go to your Hostinger dashboard
   - Navigate to **Databases** → **MySQL Databases**

2. **Create New Database**
   - Click **"Create Database"**
   - Database Name: `agnivridhi_crm` (or your preferred name)
   - Username: Create a new user or use existing
   - Password: Generate a strong password
   - **SAVE THESE CREDENTIALS!**

3. **Note Your Database Details**:
   ```
   Database Host: localhost (or provided by Hostinger)
   Database Name: u123456789_agnivridhi_crm
   Database User: u123456789_admin
   Database Password: [your-secure-password]
   Database Port: 3306
   ```

4. **Grant Privileges**
   - Ensure the user has ALL PRIVILEGES on the database
   - In phpMyAdmin, go to User Accounts and verify permissions

---

## 🔧 Step 2: Update Django Settings for MySQL

### Install MySQL Client Library

Add to `requirements.txt` (already present):
```
mysqlclient==2.2.0
```

### Update Database Configuration

The settings.py is already configured to use environment variables. You'll need to update the database section to support MySQL.

---

## 📁 Step 3: Prepare Files for Upload

### Create Production Requirements File

Create `requirements-production.txt`:
```
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.0
django-filter==23.5
mysqlclient==2.2.0
djangorestframework-simplejwt==5.3.0
WeasyPrint==60.1
Jinja2==3.1.2
Pillow==10.1.0
reportlab==4.0.7
razorpay==1.4.1
requests==2.31.0
python-decouple==3.8
openpyxl==3.1.2
xlsxwriter==3.1.9
pandas==2.1.3
numpy==1.26.2
python-dotenv==1.0.0
gunicorn==21.2.0
whitenoise==6.6.0
drf-spectacular==0.26.5
```

### Create .env File for Production

Create `.env.production`:
```env
# Django Settings
SECRET_KEY=your-super-secret-key-here-generate-new-one
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=u123456789_agnivridhi_crm
DB_USER=u123456789_admin
DB_PASSWORD=your-mysql-password-here
DB_HOST=localhost
DB_PORT=3306

# Security Settings
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
USE_X_FORWARDED_HOST=True
SECURE_PROXY_SSL_HEADER=True

# Email Configuration (Update with your SMTP details)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# WhatsApp Configuration (Optional - Twilio)
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

# Session Settings
SESSION_COOKIE_AGE=86400
SESSION_IDLE_TIMEOUT=1800
SESSION_EXPIRE_AT_BROWSER_CLOSE=False

# CORS (if you have a frontend)
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

---

## 🔐 Step 4: Generate Secret Key

Run this command locally to generate a new secret key:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and use it in your `.env.production` file.

---

## 📤 Step 5: Upload Files to Hostinger

### Via FTP/SFTP (FileZilla recommended):

1. **Connect to Hostinger**
   - Host: Your FTP hostname (from Hostinger panel)
   - Username: Your FTP username
   - Password: Your FTP password
   - Port: 21 (FTP) or 22 (SFTP)

2. **Upload Directory Structure**
   ```
   /public_html/
   └── agnivridhi_crm/
       ├── accounts/
       ├── applications/
       ├── bookings/
       ├── clients/
       ├── documents/
       ├── edit_requests/
       ├── notifications/
       ├── payments/
       ├── schemes/
       ├── activity_logs/
       ├── agnivridhi_crm/
       ├── templates/
       ├── static/
       ├── media/
       ├── manage.py
       ├── requirements-production.txt
       ├── .env (rename from .env.production)
       └── .htaccess
   ```

3. **Set Correct Permissions**
   - Directories: 755
   - Files: 644
   - manage.py: 755

---

## 🐍 Step 6: Setup Python Environment on Hostinger

### Via SSH:

1. **Connect via SSH**
   ```bash
   ssh username@yourdomain.com
   ```

2. **Navigate to Your Project**
   ```bash
   cd public_html/agnivridhi_crm
   ```

3. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements-production.txt
   ```

---

## 💾 Step 7: Database Migration

### Run Migrations:

```bash
source venv/bin/activate
cd /path/to/agnivridhi_crm

# Export database settings
export DJANGO_SETTINGS_MODULE=agnivridhi_crm.settings

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

---

## 🌐 Step 8: Configure WSGI

### Create `passenger_wsgi.py` in project root:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/username/public_html/agnivridhi_crm'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtual environment
activate_this = os.path.join(project_home, 'venv/bin/activate_this.py')
if os.path.exists(activate_this):
    exec(open(activate_this).read(), {'__file__': activate_this})

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'agnivridhi_crm.settings'

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## 🔒 Step 9: Create .htaccess File

### Create `.htaccess` in project root:

```apache
# Passenger configuration
PassengerEnabled On
PassengerPython /home/username/public_html/agnivridhi_crm/venv/bin/python
PassengerAppRoot /home/username/public_html/agnivridhi_crm

# Static files handling
<IfModule mod_rewrite.c>
    RewriteEngine On
    
    # Serve static files directly
    RewriteCond %{REQUEST_URI} ^/static/ [OR]
    RewriteCond %{REQUEST_URI} ^/media/
    RewriteRule ^(.*)$ - [L]
    
    # Forward all other requests to Django
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^(.*)$ passenger_wsgi.py [QSA,L]
</IfModule>

# Security headers
<IfModule mod_headers.c>
    Header set X-Content-Type-Options "nosniff"
    Header set X-Frame-Options "SAMEORIGIN"
    Header set X-XSS-Protection "1; mode=block"
</IfModule>
```

---

## 📊 Step 10: Verify Database Connection

### Test Database via phpMyAdmin:

1. **Login to phpMyAdmin**
2. **Select your database** (u123456789_agnivridhi_crm)
3. **Check Tables**
   - You should see tables like:
     - accounts_user
     - clients_client
     - bookings_booking
     - applications_application
     - payments_payment
     - etc.

4. **Verify Data Migration**
   - Check if your data migrated correctly
   - Run sample queries to verify

---

## 🔍 Step 11: Test Your Deployment

### Access Your Application:

1. **Visit Your Domain**
   ```
   https://yourdomain.com
   ```

2. **Test Key Functions**:
   - ✅ Login page loads
   - ✅ Can login with superuser credentials
   - ✅ Dashboard displays correctly
   - ✅ Static files (CSS/JS) load
   - ✅ Images and media files load
   - ✅ Database queries work
   - ✅ Forms submit correctly

3. **Check Django Admin**:
   ```
   https://yourdomain.com/admin/
   ```

---

## 🐛 Troubleshooting

### Common Issues:

1. **500 Internal Server Error**
   - Check error logs: `tail -f ~/logs/error.log`
   - Verify .env file exists and has correct values
   - Check file permissions
   - Verify virtual environment is activated

2. **Database Connection Error**
   - Verify MySQL credentials in .env
   - Check if database exists in phpMyAdmin
   - Ensure user has proper privileges
   - Test connection: `python manage.py dbshell`

3. **Static Files Not Loading**
   - Run: `python manage.py collectstatic`
   - Check STATIC_ROOT in settings.py
   - Verify .htaccess rules

4. **Import Errors**
   - Ensure all dependencies installed: `pip install -r requirements-production.txt`
   - Check Python version compatibility

5. **Module Not Found**
   - Verify sys.path in passenger_wsgi.py
   - Check virtual environment activation

---

## 📱 Step 12: Post-Deployment Tasks

### Essential Tasks:

1. **Create Initial Users**
   ```bash
   python manage.py createsuperuser
   ```

2. **Load Initial Data** (if you have fixtures)
   ```bash
   python manage.py loaddata initial_schemes.json
   ```

3. **Configure Email Settings**
   - Update SMTP credentials
   - Test email sending

4. **Setup Backup System**
   - Configure database backups via Hostinger
   - Schedule regular backups (daily recommended)

5. **Monitor Application**
   - Check error logs regularly
   - Monitor database size
   - Track performance

6. **SSL Certificate**
   - Enable SSL via Hostinger control panel
   - Force HTTPS redirect

---

## 🔄 Step 13: Update Settings.py for MySQL

You need to modify the DATABASES section in settings.py to use MySQL and environment variables.

The updated section should look like this:

```python
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        } if os.getenv('DB_ENGINE') == 'django.db.backends.mysql' else {},
    }
}
```

---

## 📋 Deployment Checklist

Before going live, verify:

- [ ] Database created and credentials saved
- [ ] .env file configured with production values
- [ ] SECRET_KEY generated and set
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS includes your domain
- [ ] MySQL client library installed
- [ ] All files uploaded to server
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Migrations run successfully
- [ ] Superuser created
- [ ] Static files collected
- [ ] passenger_wsgi.py configured
- [ ] .htaccess configured
- [ ] SSL certificate enabled
- [ ] Email settings tested
- [ ] Backup system configured
- [ ] All features tested on production

---

## 🆘 Support Resources

### Hostinger Documentation:
- Python App Hosting: https://support.hostinger.com/
- MySQL Database: https://support.hostinger.com/
- SSH Access: https://support.hostinger.com/

### Django Documentation:
- Deployment Checklist: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
- MySQL Configuration: https://docs.djangoproject.com/en/4.2/ref/databases/#mysql-notes

---

## 📞 Need Help?

If you encounter issues during deployment:
1. Check Hostinger error logs
2. Review Django debug output
3. Verify database connection via phpMyAdmin
4. Test each component individually
5. Contact Hostinger support for server-specific issues

---

**Last Updated**: November 10, 2025
**Django Version**: 4.2.7
**Database**: MySQL 8.0+
**Server**: Hostinger Python Hosting
