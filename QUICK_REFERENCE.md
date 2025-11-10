# 🚀 Quick Reference - Subdomain Deployment

## Your Subdomain: crm.agnivridhiindia.com

---

## 📍 Server Paths (Already Configured)

```bash
Username: u623641178
Project:  /home/u623641178/public_html/crm.agnivridhiindia.com
VEnv:     /home/u623641178/public_html/crm.agnivridhiindia.com/venv
```

---

## 🗄️ Database Credentials (Already Set)

```
Host:     localhost
Database: u623641178_CRM_AGNIVRIDHI
User:     u623641178_agnivridhi_crm
Password: Rahul@Agni121#
Port:     3306
```

---

## ✅ Pre-Deployment Checklist

### On Hostinger Panel:
- [ ] Create subdomain: `crm.agnivridhiindia.com`
  - Document Root: `/public_html/crm.agnivridhiindia.com`
- [ ] Install SSL certificate (Let's Encrypt)
- [ ] Enable Force HTTPS
- [ ] Verify DNS propagation (5-30 min)

### On Local Machine:
- [ ] Generate SECRET_KEY:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- [ ] Update SECRET_KEY in `.env.production`
- [ ] Export data (if migrating):
  ```bash
  python export_sqlite_data.py
  ```

---

## 📤 Upload Files

### FTP/SFTP Connection:
```
Host:     ftp.agnivridhiindia.com
User:     u623641178
Port:     22 (SFTP) or 21 (FTP)
```

### Upload To:
```
/public_html/crm.agnivridhiindia.com/
```

### After Upload:
1. Rename `.env.production` to `.env`
2. Delete `.env.production`
3. Upload `backup_data/` folder (if migrating)

---

## 🔧 SSH Deployment

### Connect:
```bash
ssh u623641178@agnivridhiindia.com
```

### Quick Deploy:
```bash
cd ~/public_html/crm.agnivridhiindia.com
chmod +x deploy-hostinger.sh
./deploy-hostinger.sh
```

### Manual Deploy:
```bash
cd ~/public_html/crm.agnivridhiindia.com

# Setup
python3.9 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements-production.txt

# Database
python manage.py migrate
python manage.py createsuperuser

# Static files
python manage.py collectstatic --noinput

# Permissions
chmod -R 755 .
chmod 600 .env

# Import data (if migrating)
python import_to_mysql.py
```

---

## 🧪 Test URLs

- **Homepage:** https://crm.agnivridhiindia.com
- **Login:** https://crm.agnivridhiindia.com/login/
- **Admin:** https://crm.agnivridhiindia.com/admin/
- **Dashboard:** https://crm.agnivridhiindia.com/dashboard/
- **API Docs:** https://crm.agnivridhiindia.com/api/docs/

---

## 🔄 Common Commands

### Restart Application:
```bash
cd ~/public_html/crm.agnivridhiindia.com
mkdir -p tmp && touch tmp/restart.txt
```

### View Logs:
```bash
tail -f ~/logs/error.log
tail -f ~/logs/crm.agnivridhiindia.com-error.log
```

### Update Code:
```bash
cd ~/public_html/crm.agnivridhiindia.com
source venv/bin/activate
pip install -r requirements-production.txt
python manage.py migrate
python manage.py collectstatic --noinput
mkdir -p tmp && touch tmp/restart.txt
```

### Database Shell:
```bash
cd ~/public_html/crm.agnivridhiindia.com
source venv/bin/activate
python manage.py dbshell
```

### Check Status:
```bash
cd ~/public_html/crm.agnivridhiindia.com
source venv/bin/activate
python manage.py check
python manage.py showmigrations
```

---

## 🐛 Troubleshooting

### 500 Error:
```bash
tail -50 ~/logs/error.log
cd ~/public_html/crm.agnivridhiindia.com
cat .env  # verify settings
```

### Static Files Not Loading:
```bash
cd ~/public_html/crm.agnivridhiindia.com
source venv/bin/activate
python manage.py collectstatic --noinput
chmod -R 755 staticfiles/
mkdir -p tmp && touch tmp/restart.txt
```

### Database Connection Failed:
```bash
mysql -u u623641178_agnivridhi_crm -p u623641178_CRM_AGNIVRIDHI
# Password: Rahul@Agni121#
```

### Permissions Error:
```bash
cd ~/public_html
chmod -R 755 crm.agnivridhiindia.com/
chmod 600 crm.agnivridhiindia.com/.env
```

---

## 📧 Email Setup

Update in `.env`:
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@agnivridhiindia.com
```

Gmail App Password: https://myaccount.google.com/apppasswords

---

## ✅ Files Updated for Subdomain

All configuration files are already updated:
- ✅ `.env.production` → ALLOWED_HOSTS includes `crm.agnivridhiindia.com`
- ✅ `passenger_wsgi.py` → Paths updated to subdomain
- ✅ `.htaccess` → Passenger config updated to subdomain
- ✅ `deploy-hostinger.sh` → Project directory updated

---

## 🎯 Quick Deployment Steps

1. **On Hostinger Panel:**
   - Create subdomain `crm.agnivridhiindia.com`
   - Install SSL certificate
   - Enable HTTPS redirect

2. **Upload Files:**
   - Connect via FTP to `/public_html/crm.agnivridhiindia.com/`
   - Upload all files
   - Rename `.env.production` to `.env`

3. **Deploy via SSH:**
   ```bash
   ssh u623641178@agnivridhiindia.com
   cd ~/public_html/crm.agnivridhiindia.com
   chmod +x deploy-hostinger.sh
   ./deploy-hostinger.sh
   ```

4. **Test:**
   - Visit https://crm.agnivridhiindia.com
   - Login with superuser
   - Verify all features work

---

## 📞 Emergency Contacts

**Hostinger Support:** 24/7 Live Chat
**Check Logs:** `tail -f ~/logs/error.log`
**Restart App:** `cd ~/public_html/crm.agnivridhiindia.com && mkdir -p tmp && touch tmp/restart.txt`

---

**Total Deployment Time:** ~20-30 minutes
**Status:** Ready to Deploy! 🚀
