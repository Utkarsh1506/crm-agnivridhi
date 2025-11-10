# 🚀 Hostinger Deployment - Complete Checklist

## ✅ Pre-Deployment (On Your Local Machine)

### 1. Database Setup
- [ ] Export existing SQLite data: `python export_sqlite_data.py`
- [ ] Verify backup_data/ folder contains all JSON files
- [ ] Test export completeness

### 2. Configuration Files
- [ ] Generate new SECRET_KEY for production
- [ ] Update `.env.production` with:
  - [ ] MySQL database credentials
  - [ ] Your domain name in ALLOWED_HOSTS
  - [ ] Email SMTP settings
  - [ ] Set DEBUG=False
  - [ ] Set security headers to True
- [ ] Update `passenger_wsgi.py` with your Hostinger username
- [ ] Update `.htaccess` with your Hostinger username
- [ ] Update `deploy-hostinger.sh` with your paths

### 3. Code Review
- [ ] All migrations created: `python manage.py makemigrations`
- [ ] Test locally one final time
- [ ] Commit all changes to Git (optional but recommended)
- [ ] Create project ZIP/TAR for upload

---

## 🌐 Hostinger Setup

### 1. Database Creation
- [ ] Login to Hostinger Control Panel
- [ ] Navigate to Databases → MySQL Databases
- [ ] Create new database:
  - Database name: `u123456789_agnivridhi_crm`
  - Username: `u123456789_admin`
  - Strong password generated
- [ ] **SAVE CREDENTIALS SECURELY**
- [ ] Verify database appears in phpMyAdmin
- [ ] Check user has ALL PRIVILEGES

### 2. SSH Access
- [ ] Enable SSH in Hostinger panel
- [ ] Note SSH hostname
- [ ] Note SSH username
- [ ] Note SSH port (usually 22)
- [ ] Test SSH connection: `ssh username@hostname`

### 3. Domain Configuration
- [ ] Domain DNS pointing to Hostinger
- [ ] SSL certificate enabled
- [ ] Force HTTPS enabled
- [ ] Test domain resolves correctly

---

## 📤 File Upload

### 1. Upload via FTP/SFTP
- [ ] Connect to Hostinger FTP/SFTP
- [ ] Navigate to `/public_html/`
- [ ] Create folder: `agnivridhi_crm`
- [ ] Upload all project files to `/public_html/agnivridhi_crm/`
- [ ] Upload `backup_data/` folder (with exported data)
- [ ] Rename `.env.production` to `.env`
- [ ] Verify all files uploaded completely

### 2. Check File Structure
```
/public_html/agnivridhi_crm/
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
├── backup_data/          ← Your exported data
├── manage.py
├── passenger_wsgi.py
├── .htaccess
├── .env                   ← Renamed from .env.production
├── requirements-production.txt
└── deploy-hostinger.sh
```

### 3. Set Permissions
- [ ] Directories: 755
- [ ] Files: 644
- [ ] .env: 600 (read-only for owner)
- [ ] deploy-hostinger.sh: 755 (executable)

---

## 🔧 Server Configuration (via SSH)

### 1. Connect to Server
```bash
ssh u123456789@yourdomain.com
cd ~/public_html/agnivridhi_crm
```

### 2. Python Environment
- [ ] Check Python version: `python3.9 --version`
- [ ] Create virtual environment: `python3.9 -m venv venv`
- [ ] Activate venv: `source venv/bin/activate`
- [ ] Upgrade pip: `pip install --upgrade pip`

### 3. Install Dependencies
- [ ] Install requirements: `pip install -r requirements-production.txt`
- [ ] Verify MySQL client: `python -c "import MySQLdb; print('MySQL OK')"`
- [ ] Check all imports work

### 4. Database Setup
- [ ] Test database connection: `python manage.py dbshell`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Verify tables created in phpMyAdmin
- [ ] Import data: `python import_to_mysql.py`
- [ ] Create superuser: `python manage.py createsuperuser`

### 5. Static Files
- [ ] Collect static files: `python manage.py collectstatic --noinput`
- [ ] Verify staticfiles/ folder created
- [ ] Check static files accessible

### 6. File Permissions (Final)
```bash
chmod -R 755 ~/public_html/agnivridhi_crm
chmod 600 ~/public_html/agnivridhi_crm/.env
chmod 644 ~/public_html/agnivridhi_crm/passenger_wsgi.py
chmod 644 ~/public_html/agnivridhi_crm/.htaccess
```

---

## 🧪 Testing

### 1. Initial Access
- [ ] Visit: `https://yourdomain.com`
- [ ] Homepage loads without errors
- [ ] No 500/404 errors
- [ ] SSL certificate valid (padlock shows)

### 2. Static Files
- [ ] CSS loads correctly (page styled)
- [ ] JavaScript works (dropdowns, modals)
- [ ] Images display
- [ ] Bootstrap icons show

### 3. Authentication
- [ ] Login page loads: `/login/`
- [ ] Can login with superuser
- [ ] Dashboard redirects correctly
- [ ] Logout works

### 4. Database Operations
- [ ] Can view existing clients
- [ ] Can create new records
- [ ] Can edit records
- [ ] Can delete records
- [ ] Search functionality works

### 5. Features Testing
- [ ] Client creation works
- [ ] Booking records work
- [ ] Applications submission works
- [ ] Payments recording works
- [ ] Document uploads work
- [ ] Edit requests work
- [ ] Activity feed displays
- [ ] Notifications work

### 6. Admin Panel
- [ ] Access: `https://yourdomain.com/admin/`
- [ ] Can login
- [ ] All models visible
- [ ] Can perform CRUD operations

### 7. API Testing (if using)
- [ ] API endpoints accessible
- [ ] Swagger docs work: `/api/docs/`
- [ ] Authentication works
- [ ] GET/POST requests work

---

## 🔐 Security Check

### 1. Settings Verification
- [ ] DEBUG=False in production
- [ ] SECRET_KEY is unique and secure
- [ ] ALLOWED_HOSTS configured correctly
- [ ] CSRF protection enabled
- [ ] Session cookies secure
- [ ] Security headers enabled

### 2. File Security
- [ ] .env file not accessible via web
- [ ] .git folder not uploaded (or protected)
- [ ] manage.py not web-accessible
- [ ] Database file not web-accessible

### 3. Database Security
- [ ] Strong MySQL password
- [ ] User has only necessary privileges
- [ ] No default passwords in use
- [ ] Backup system enabled

### 4. SSL/HTTPS
- [ ] SSL certificate active
- [ ] HTTPS redirect working
- [ ] Mixed content warnings resolved
- [ ] HSTS header set

---

## 📊 Post-Deployment

### 1. Monitoring Setup
- [ ] Check error logs: `tail -f ~/logs/error.log`
- [ ] Setup uptime monitoring (UptimeRobot, etc.)
- [ ] Configure log rotation
- [ ] Setup alerts for errors

### 2. Backup Configuration
- [ ] Enable automatic database backups (Hostinger panel)
- [ ] Set backup frequency (daily recommended)
- [ ] Test backup restoration
- [ ] Download local copy of backup

### 3. Performance Optimization
- [ ] Enable gzip compression (.htaccess)
- [ ] Set cache headers
- [ ] Optimize database queries
- [ ] Consider CDN for static files

### 4. Documentation
- [ ] Document admin credentials (securely)
- [ ] Create user manual (if needed)
- [ ] Document deployment process
- [ ] Note any custom configurations

### 5. User Setup
- [ ] Create manager accounts
- [ ] Create sales employee accounts
- [ ] Test different role permissions
- [ ] Send login credentials to users

---

## 🆘 Troubleshooting Guide

### Issue: 500 Internal Server Error
- [ ] Check: `tail -f ~/logs/error.log`
- [ ] Check: `.env` file exists and has correct values
- [ ] Check: Virtual environment activated
- [ ] Check: All dependencies installed
- [ ] Restart: `mkdir -p tmp && touch tmp/restart.txt`

### Issue: Database Connection Error
- [ ] Verify MySQL credentials in `.env`
- [ ] Test connection: `python manage.py dbshell`
- [ ] Check database exists in phpMyAdmin
- [ ] Verify user privileges
- [ ] Check DB_HOST (usually 'localhost')

### Issue: Static Files Not Loading (404)
- [ ] Run: `python manage.py collectstatic --noinput`
- [ ] Check STATIC_ROOT path
- [ ] Verify .htaccess rules
- [ ] Check file permissions: `chmod -R 755 staticfiles/`
- [ ] Check STATIC_URL in settings

### Issue: Import Errors
- [ ] Activate venv: `source venv/bin/activate`
- [ ] Reinstall: `pip install -r requirements-production.txt`
- [ ] Check Python version compatibility
- [ ] Verify sys.path in passenger_wsgi.py

### Issue: Permission Denied
- [ ] Check file permissions
- [ ] Ensure user owns files: `chown -R username:username *`
- [ ] Check directory permissions: 755
- [ ] Check file permissions: 644

### Issue: Page Not Found (404)
- [ ] Check URL patterns in urls.py
- [ ] Verify .htaccess rules
- [ ] Check domain DNS
- [ ] Clear browser cache

### Need to Restart Application
```bash
mkdir -p ~/public_html/agnivridhi_crm/tmp
touch ~/public_html/agnivridhi_crm/tmp/restart.txt
```

---

## ✅ Final Verification

### Pre-Launch Checklist
- [ ] All features tested and working
- [ ] No error messages in logs
- [ ] SSL certificate valid
- [ ] All pages load correctly
- [ ] Static files loading
- [ ] Database queries working
- [ ] Email sending configured
- [ ] Backups configured
- [ ] Monitoring setup
- [ ] Admin credentials secure
- [ ] User accounts created
- [ ] Documentation complete

### Go Live!
- [ ] Announce to team
- [ ] Monitor for first 24 hours
- [ ] Check error logs regularly
- [ ] Gather user feedback
- [ ] Address any issues promptly

---

## 📞 Support Contacts

**Hostinger Support:**
- Live Chat: Available 24/7 via panel
- Email: support@hostinger.com
- Knowledge Base: support.hostinger.com

**Django Documentation:**
- Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
- MySQL: https://docs.djangoproject.com/en/4.2/ref/databases/#mysql-notes

**Emergency Commands:**
```bash
# View error logs
tail -f ~/logs/error.log

# Restart application
mkdir -p tmp && touch tmp/restart.txt

# Test database
python manage.py dbshell

# Check migrations
python manage.py showmigrations

# Collect static files
python manage.py collectstatic --noinput
```

---

**Last Updated:** November 10, 2025
**Status:** Ready for Deployment
**Estimated Time:** 30-45 minutes total
