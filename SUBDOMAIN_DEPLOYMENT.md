# 🌐 Subdomain Deployment Guide - crm.agnivridhiindia.com

## Overview
This guide is specifically for deploying your Agnivridhi CRM on the subdomain: **crm.agnivridhiindia.com**

---

## 📋 Step 1: Create Subdomain on Hostinger

### Via Hostinger Control Panel:

1. **Login to Hostinger**
   - Go to your Hostinger dashboard
   - Navigate to **Domains** section

2. **Create Subdomain**
   - Click on your domain: `agnivridhiindia.com`
   - Go to **Subdomains** section
   - Click **"Create Subdomain"**
   - Subdomain name: `crm`
   - Full subdomain: `crm.agnivridhiindia.com`
   - Document root: `/public_html/crm.agnivridhiindia.com`
   - Click **Create**

3. **Verify Subdomain**
   - Subdomain should appear in your list
   - DNS propagation may take 5-30 minutes
   - Test by visiting: `http://crm.agnivridhiindia.com` (will show empty/404 initially)

---

## 🔐 Step 2: Enable SSL for Subdomain

1. **Go to SSL/TLS in Hostinger**
   - Navigate to **SSL/TLS** section
   - Find your subdomain: `crm.agnivridhiindia.com`

2. **Install SSL Certificate**
   - Click **Install SSL**
   - Choose **Free SSL (Let's Encrypt)** 
   - Or use your existing wildcard certificate
   - Wait for installation to complete

3. **Enable Force HTTPS**
   - Enable **Force HTTPS Redirect**
   - This ensures all traffic uses HTTPS

4. **Verify SSL**
   - Visit: `https://crm.agnivridhiindia.com`
   - Check for padlock icon in browser
   - Certificate should be valid

---

## 📁 Step 3: Directory Structure on Server

Your subdomain will be located at:
```
/home/u623641178/public_html/crm.agnivridhiindia.com/
```

This is different from your main domain:
- Main domain: `/public_html/` or `/public_html/agnivridhiindia.com/`
- Subdomain: `/public_html/crm.agnivridhiindia.com/`

---

## 🗄️ Step 4: MySQL Database (Already Created)

Your database is already configured:
```
Database: u623641178_CRM_AGNIVRIDHI
Username: u623641178_agnivridhi_crm
Password: Rahul@Agni121#
Host: localhost
Port: 3306
```

**No additional database setup needed!** ✅

---

## 📤 Step 5: Upload Files via FTP/SFTP

### Connection Details:
```
Protocol: SFTP (or FTP)
Host: ftp.agnivridhiindia.com
Username: u623641178
Password: [Your FTP password]
Port: 22 (SFTP) or 21 (FTP)
```

### Upload Structure:
1. **Connect to FTP/SFTP**
2. **Navigate to**: `/public_html/`
3. **Create directory** (if not exists): `crm.agnivridhiindia.com`
4. **Upload all files to**: `/public_html/crm.agnivridhiindia.com/`

### Files to Upload:
```
/public_html/crm.agnivridhiindia.com/
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
├── backup_data/          (if migrating data)
├── manage.py
├── passenger_wsgi.py     ✅ Updated with subdomain paths
├── .htaccess             ✅ Updated with subdomain paths
├── .env.production       ✅ Updated with subdomain
├── requirements-production.txt
└── deploy-hostinger.sh   ✅ Updated with subdomain paths
```

### Important:
- **Rename** `.env.production` to `.env` after upload
- **Delete** `.env.production` after renaming
- **Check** all files uploaded completely

---

## 🔧 Step 6: Deploy via SSH

### Connect to SSH:
```bash
ssh u623641178@agnivridhiindia.com
# Or
ssh u623641178@crm.agnivridhiindia.com
```

### Navigate to Project:
```bash
cd ~/public_html/crm.agnivridhiindia.com
```

### Run Deployment Script:
```bash
chmod +x deploy-hostinger.sh
./deploy-hostinger.sh
```

### Or Deploy Manually:
```bash
# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements-production.txt

# Setup database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Set permissions
chmod -R 755 ~/public_html/crm.agnivridhiindia.com
chmod 600 ~/public_html/crm.agnivridhiindia.com/.env
```

---

## 🧪 Step 7: Test Your Subdomain

### Access Your CRM:
1. **Visit**: `https://crm.agnivridhiindia.com`
2. **Check**:
   - ✅ Homepage loads without errors
   - ✅ SSL certificate valid (padlock shown)
   - ✅ No 500 errors
   - ✅ Login page accessible

3. **Test Features**:
   - ✅ Login with superuser
   - ✅ Dashboard displays
   - ✅ Static files load (CSS/JS)
   - ✅ Can create/view clients
   - ✅ All navigation works

### Admin Panel:
- **URL**: `https://crm.agnivridhiindia.com/admin/`
- **Login**: Your superuser credentials
- **Verify**: All models accessible

---

## 🔄 Step 8: Import Data (If Migrating)

If you're migrating from local SQLite:

1. **On Local Machine** (before upload):
   ```bash
   python export_sqlite_data.py
   ```
   This creates `backup_data/` folder

2. **Upload** `backup_data/` folder to server

3. **On Server** (via SSH):
   ```bash
   cd ~/public_html/crm.agnivridhiindia.com
   source venv/bin/activate
   python import_to_mysql.py
   ```

---

## 🔄 Restart Application

Whenever you make changes, restart the application:

```bash
cd ~/public_html/crm.agnivridhiindia.com
mkdir -p tmp && touch tmp/restart.txt
```

Or via SSH:
```bash
ssh u623641178@agnivridhiindia.com "cd public_html/crm.agnivridhiindia.com && mkdir -p tmp && touch tmp/restart.txt"
```

---

## 🐛 Troubleshooting

### Issue: Subdomain Shows 404 or Directory Listing

**Solution:**
1. Verify subdomain created correctly
2. Check document root: `/public_html/crm.agnivridhiindia.com`
3. Ensure `.htaccess` file exists
4. Check `passenger_wsgi.py` exists

### Issue: 500 Internal Server Error

**Solution:**
```bash
# Check error logs
tail -f ~/logs/crm.agnivridhiindia.com-error.log
# Or general logs
tail -f ~/logs/error.log

# Verify .env file
cat ~/public_html/crm.agnivridhiindia.com/.env

# Check virtual environment
source ~/public_html/crm.agnivridhiindia.com/venv/bin/activate
python --version
python -c "import django; print(django.get_version())"
```

### Issue: Static Files Not Loading

**Solution:**
```bash
cd ~/public_html/crm.agnivridhiindia.com
source venv/bin/activate
python manage.py collectstatic --noinput
chmod -R 755 staticfiles/
```

### Issue: Database Connection Error

**Solution:**
1. Verify credentials in `.env` file
2. Test connection:
   ```bash
   mysql -u u623641178_agnivridhi_crm -p -h localhost u623641178_CRM_AGNIVRIDHI
   ```
3. Check user privileges in phpMyAdmin

### Issue: Permission Denied

**Solution:**
```bash
cd ~/public_html
chmod -R 755 crm.agnivridhiindia.com/
chown -R u623641178:u623641178 crm.agnivridhiindia.com/
chmod 600 crm.agnivridhiindia.com/.env
```

---

## 🔐 Security Checklist

Before going live:

- [x] SSL certificate installed and working
- [x] HTTPS force redirect enabled
- [x] DEBUG=False in .env
- [x] Strong SECRET_KEY generated
- [x] Database password secure
- [x] .env file permissions: 600
- [x] ALLOWED_HOSTS includes subdomain
- [x] Security headers enabled in .htaccess

---

## 📊 Configuration Summary

### Your Subdomain Configuration:

**URLs:**
- Production: `https://crm.agnivridhiindia.com`
- Admin: `https://crm.agnivridhiindia.com/admin/`
- API Docs: `https://crm.agnivridhiindia.com/api/docs/`

**Server Paths:**
- Project Root: `/home/u623641178/public_html/crm.agnivridhiindia.com`
- Virtual Env: `/home/u623641178/public_html/crm.agnivridhiindia.com/venv`
- Static Files: `/home/u623641178/public_html/crm.agnivridhiindia.com/staticfiles`
- Media Files: `/home/u623641178/public_html/crm.agnivridhiindia.com/media`

**Database:**
- Host: localhost
- Database: u623641178_CRM_AGNIVRIDHI
- User: u623641178_agnivridhi_crm
- Port: 3306

**Environment Variables (.env):**
```env
ALLOWED_HOSTS=crm.agnivridhiindia.com,agnivridhiindia.com,www.agnivridhiindia.com
DB_NAME=u623641178_CRM_AGNIVRIDHI
DB_USER=u623641178_agnivridhi_crm
DB_PASSWORD=Rahul@Agni121#
```

---

## 📧 Email Configuration

Update email settings in your `.env` file:

```env
EMAIL_HOST_USER=crm@agnivridhiindia.com
EMAIL_HOST_PASSWORD=your-email-app-password
DEFAULT_FROM_EMAIL=noreply@agnivridhiindia.com
```

For Gmail:
1. Enable 2-factor authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use app password in EMAIL_HOST_PASSWORD

---

## 🚀 Quick Commands Reference

### Deploy/Update:
```bash
cd ~/public_html/crm.agnivridhiindia.com
source venv/bin/activate
git pull  # if using git
pip install -r requirements-production.txt
python manage.py migrate
python manage.py collectstatic --noinput
mkdir -p tmp && touch tmp/restart.txt
```

### Check Status:
```bash
cd ~/public_html/crm.agnivridhiindia.com
source venv/bin/activate
python manage.py check
python manage.py showmigrations
```

### View Logs:
```bash
tail -f ~/logs/crm.agnivridhiindia.com-error.log
tail -f ~/logs/error.log
```

### Database Shell:
```bash
cd ~/public_html/crm.agnivridhiindia.com
source venv/bin/activate
python manage.py dbshell
```

---

## 🎯 Post-Deployment Tasks

1. **Test All Features**:
   - [ ] User authentication
   - [ ] Client management
   - [ ] Booking creation
   - [ ] Application submission
   - [ ] Payment recording
   - [ ] Document uploads
   - [ ] Email notifications
   - [ ] Activity logging

2. **Create User Accounts**:
   - [ ] Create manager accounts
   - [ ] Create sales employee accounts
   - [ ] Test role permissions
   - [ ] Send credentials to users

3. **Setup Monitoring**:
   - [ ] Setup uptime monitoring (UptimeRobot)
   - [ ] Configure error alerts
   - [ ] Regular backup checks

4. **Documentation**:
   - [ ] Document admin credentials
   - [ ] Create user guide
   - [ ] Note any custom configurations

---

## 📞 Support

**Hostinger Support:**
- Live Chat: Available 24/7
- Ticket System: Via control panel

**Check Logs:**
```bash
# Application errors
tail -100 ~/logs/error.log

# Subdomain specific
tail -100 ~/logs/crm.agnivridhiindia.com-error.log

# Access logs
tail -100 ~/logs/access.log
```

---

**Last Updated:** November 10, 2025
**Subdomain:** crm.agnivridhiindia.com
**Status:** Ready for Deployment ✅
