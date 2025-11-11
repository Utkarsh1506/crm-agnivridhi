# 🚀 PythonAnywhere Deployment Guide - Agnivridhi CRM

**Much simpler than Hostinger! PythonAnywhere is designed for Django.**

---

## ✅ Advantages of PythonAnywhere

- ✅ Python 3.10+ available (Django 4.2.7 compatible)
- ✅ MySQL database included (even on free tier)
- ✅ Built-in web interface for configuration
- ✅ Static files served automatically
- ✅ Git deployment built-in
- ✅ HTTPS/SSL included
- ✅ Easy reload/restart
- ✅ No complex server configuration

---

## 📋 Step-by-Step Deployment

### Step 1: Create PythonAnywhere Account

1. Go to: https://www.pythonanywhere.com/
2. Sign up for an account (Free or Paid)
3. Choose your username (e.g., `agnivridhi`)
4. Your app will be at: `https://agnivridhi.pythonanywhere.com`

**Note:** For custom domain (crm.agnivridhiindia.com), you need a paid account ($5/month minimum).

---

### Step 2: Upload Your Code

**Option A: Git Clone (Recommended)**

1. Open "Consoles" tab → Start a Bash console
2. Clone your repository:
   ```bash
   git clone https://github.com/Utkarsh1506/crm-agnivridhi.git
   cd crm-agnivridhi
   ```

**Option B: Upload Files**

1. Go to "Files" tab
2. Create directory: `/home/agnivridhi/crm-agnivridhi`
3. Upload all files using the upload button

---

### Step 3: Create MySQL Database

1. Go to "Databases" tab
2. Click "Initialize MySQL"
3. Set a password for your MySQL database
4. Create a new database:
   - Database name: `agnivridhi$crm_agnivridhi`
   - Note: PythonAnywhere adds your username prefix automatically

**Save these credentials:**
- Database: `agnivridhi$crm_agnivridhi`
- Username: `agnivridhi`
- Password: [the password you set]
- Host: `agnivridhi.mysql.pythonanywhere-services.com`

---

### Step 4: Create Virtual Environment

Open a Bash console and run:

```bash
cd ~/crm-agnivridhi

# Create virtual environment with Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 crm-env

# Activate it (if not already active)
workon crm-env

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

---

### Step 5: Configure Environment Variables

Create `.env` file in your project:

```bash
cd ~/crm-agnivridhi
nano .env
```

Paste this (replace with your MySQL credentials):

```env
# Django Settings
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=agnivridhi.pythonanywhere.com,www.agnivridhi.pythonanywhere.com

# MySQL Database (PythonAnywhere)
DB_ENGINE=django.db.backends.mysql
DB_NAME=agnivridhi$crm_agnivridhi
DB_USER=agnivridhi
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_HOST=agnivridhi.mysql.pythonanywhere-services.com
DB_PORT=3306

# Security (Production)
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@agnivridhiindia.com

# Static/Media Files
STATIC_ROOT=/home/agnivridhi/crm-agnivridhi/staticfiles
MEDIA_ROOT=/home/agnivridhi/crm-agnivridhi/media

# Twilio (Optional)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Save and exit (Ctrl+O, Enter, Ctrl+X)

Set permissions:
```bash
chmod 600 .env
```

---

### Step 6: Run Database Migrations

```bash
cd ~/crm-agnivridhi
workon crm-env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

---

### Step 7: Configure Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration" (NOT Django wizard)
4. Select Python 3.10

**Configure these sections:**

#### A. Source Code
```
/home/agnivridhi/crm-agnivridhi
```

#### B. Working Directory
```
/home/agnivridhi/crm-agnivridhi
```

#### C. Virtualenv
```
/home/agnivridhi/.virtualenvs/crm-env
```

#### D. WSGI Configuration File
Click on the WSGI file link and replace ALL contents with:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/agnivridhi/crm-agnivridhi'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'agnivridhi_crm.settings'

# Load environment from .env file
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path('/home/agnivridhi/crm-agnivridhi/.env'))

# Initialize Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Save the file.

---

### Step 8: Configure Static Files Mapping

In the "Web" tab, scroll to "Static files" section:

Add these mappings:

| URL              | Directory                                          |
|------------------|----------------------------------------------------|
| `/static/`       | `/home/agnivridhi/crm-agnivridhi/staticfiles`     |
| `/media/`        | `/home/agnivridhi/crm-agnivridhi/media`           |

---

### Step 9: Reload Your Web App

1. Scroll to top of "Web" tab
2. Click the big green **"Reload"** button
3. Wait 30 seconds

---

### Step 10: Test Your Application

Visit: `https://agnivridhi.pythonanywhere.com`

Test these URLs:
- `/` - Homepage
- `/admin/` - Admin login
- `/login/` - CRM login

---

## 🔧 Common Commands

### Reload the App (After Code Changes)
Go to "Web" tab → Click "Reload" button

Or via console:
```bash
touch /var/www/agnivridhi_pythonanywhere_com_wsgi.py
```

### View Error Logs
Go to "Web" tab → Scroll to "Log files" section → Click "Error log"

### Update Code from Git
```bash
cd ~/crm-agnivridhi
git pull origin main
workon crm-env
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
# Then reload web app
```

### Access Django Shell
```bash
cd ~/crm-agnivridhi
workon crm-env
python manage.py shell
```

### Run Management Commands
```bash
cd ~/crm-agnivridhi
workon crm-env
python manage.py your_command
```

---

## 🌐 Custom Domain Setup (Paid Plans Only)

If you have a paid PythonAnywhere account:

### 1. Update DNS Records

Add CNAME record in your domain DNS:
```
crm.agnivridhiindia.com → agnivridhi.pythonanywhere.com
```

### 2. Configure in PythonAnywhere

1. Go to "Web" tab
2. In "Configuration for" section, add custom domain:
   - Domain name: `crm.agnivridhiindia.com`
3. Update ALLOWED_HOSTS in `.env`:
   ```env
   ALLOWED_HOSTS=crm.agnivridhiindia.com,agnivridhi.pythonanywhere.com
   ```
4. Reload web app

### 3. SSL Certificate (Free)

PythonAnywhere automatically provides SSL for custom domains.

---

## 📊 Database Management

### phpMyAdmin Alternative

PythonAnywhere provides:
1. Go to "Databases" tab
2. Click "Start a console on your MySQL database"
3. Or use MySQL Workbench with SSH tunnel

### Backup Database

```bash
mysqldump -u agnivridhi -h agnivridhi.mysql.pythonanywhere-services.com -p 'agnivridhi$crm_agnivridhi' > backup.sql
```

### Restore Database

```bash
mysql -u agnivridhi -h agnivridhi.mysql.pythonanywhere-services.com -p 'agnivridhi$crm_agnivridhi' < backup.sql
```

---

## 🆘 Troubleshooting

### ImportError: No module named 'X'
```bash
workon crm-env
pip install X
# Reload web app
```

### 500 Internal Server Error
Check error log in "Web" tab → "Log files" section

### Static files not loading
```bash
python manage.py collectstatic --noinput
# Check Static files mapping in Web tab
# Reload web app
```

### Database connection error
- Verify MySQL credentials in `.env`
- Check database exists in "Databases" tab
- Ensure DB_HOST is correct: `agnivridhi.mysql.pythonanywhere-services.com`

---

## 💰 Pricing

**Free Tier:**
- 1 web app
- 512 MB disk space
- MySQL database (200 MB)
- `username.pythonanywhere.com` domain
- Good for testing!

**Hacker Plan ($5/month):**
- Custom domain (crm.agnivridhiindia.com)
- 1 GB disk space
- MySQL database (1 GB)
- SSH access
- Always-on tasks

**Web Dev Plan ($12/month):**
- Multiple web apps
- 2 GB disk space
- 3 GB MySQL
- Better performance

---

## 🎯 Quick Deployment Checklist

- [ ] Create PythonAnywhere account
- [ ] Upload/clone code to `/home/agnivridhi/crm-agnivridhi`
- [ ] Create MySQL database in "Databases" tab
- [ ] Create virtualenv with Python 3.10
- [ ] Install requirements.txt
- [ ] Create and configure .env file
- [ ] Run migrations
- [ ] Create superuser
- [ ] Collect static files
- [ ] Configure web app in "Web" tab
- [ ] Update WSGI file
- [ ] Add static files mappings
- [ ] Reload web app
- [ ] Test application
- [ ] (Optional) Configure custom domain

---

## 📞 Support

- **PythonAnywhere Help:** https://help.pythonanywhere.com/
- **Forums:** https://www.pythonanywhere.com/forums/
- **Email:** support@pythonanywhere.com

---

## ✅ Advantages Over Hostinger

| Feature              | PythonAnywhere          | Hostinger             |
|----------------------|-------------------------|-----------------------|
| Setup Complexity     | ⭐⭐⭐⭐⭐ Very Easy   | ⭐⭐ Difficult        |
| Python Version       | 3.10+                   | 3.6 (outdated)        |
| Django Support       | Native                  | Via Passenger (tricky)|
| Database Setup       | One-click MySQL         | Manual configuration  |
| Static Files         | Automatic               | Manual collectstatic  |
| SSL/HTTPS            | Automatic               | Manual setup          |
| Reload/Restart       | One button              | Touch restart.txt     |
| Error Logs           | Web interface           | SSH + file hunting    |
| Virtual Environment  | Built-in `mkvirtualenv` | Manual setup          |

**Verdict:** PythonAnywhere is 10x easier for Django projects! 🎉

---

Good luck with your deployment! Let me know if you need help with any step.
