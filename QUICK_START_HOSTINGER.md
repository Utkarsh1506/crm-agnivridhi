# Quick Start - Hostinger Deployment

## 🚀 Fast Track Deployment (15 Minutes)

### 1️⃣ Prepare on Hostinger (5 minutes)

**A. Create MySQL Database**
1. Login to Hostinger → Databases → MySQL Databases
2. Click "Create Database"
3. Note these details:
   ```
   Database: u123456789_agnivridhi_crm
   Username: u123456789_admin
   Password: [generated-password]
   Host: localhost
   ```

**B. Get SSH Access**
1. Hostinger Panel → Advanced → SSH Access
2. Enable SSH
3. Note SSH credentials

---

### 2️⃣ Configure Files Locally (5 minutes)

**A. Update `.env.production`**
```bash
# Open .env.production and update:
DB_NAME=u123456789_agnivridhi_crm
DB_USER=u123456789_admin
DB_PASSWORD=your-actual-password
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

**B. Generate Secret Key**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy output to `.env.production` SECRET_KEY

**C. Update Paths in Files**
Replace `u123456789` with YOUR actual Hostinger username in:
- `passenger_wsgi.py`
- `.htaccess`
- `deploy-hostinger.sh`

---

### 3️⃣ Upload to Hostinger (3 minutes)

**Via FTP/SFTP (FileZilla):**

1. Connect:
   - Host: `ftp.yourdomain.com`
   - Username: Your FTP username
   - Password: Your FTP password
   - Port: 21 (FTP) or 22 (SFTP)

2. Upload entire project folder to:
   ```
   /public_html/agnivridhi_crm/
   ```

3. **IMPORTANT**: Rename `.env.production` to `.env` on server

---

### 4️⃣ Deploy via SSH (2 minutes)

**Connect to SSH:**
```bash
ssh u123456789@yourdomain.com
```

**Run deployment script:**
```bash
cd ~/public_html/agnivridhi_crm
chmod +x deploy-hostinger.sh
./deploy-hostinger.sh
```

**Or manually:**
```bash
cd ~/public_html/agnivridhi_crm
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements-production.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

### 5️⃣ Test & Launch

**Visit your site:**
```
https://yourdomain.com
```

**Test:**
- ✅ Homepage loads
- ✅ Login works
- ✅ Dashboard displays
- ✅ Static files load (CSS/JS)
- ✅ Database queries work

**If issues, restart app:**
```bash
cd ~/public_html/agnivridhi_crm
mkdir -p tmp && touch tmp/restart.txt
```

---

## 📋 Pre-Flight Checklist

Before deployment:
- [ ] MySQL database created on Hostinger
- [ ] SSH access enabled
- [ ] `.env.production` configured with real values
- [ ] Secret key generated
- [ ] Hostinger username updated in all config files
- [ ] Domain DNS pointing to Hostinger
- [ ] SSL certificate enabled (via Hostinger panel)

---

## 🐛 Quick Troubleshooting

**500 Error:**
```bash
tail -f ~/logs/error.log
```

**Database Connection Failed:**
```bash
python manage.py dbshell  # Test connection
```

**Static Files Not Loading:**
```bash
python manage.py collectstatic --noinput
chmod -R 755 staticfiles/
```

**Restart Application:**
```bash
mkdir -p tmp && touch tmp/restart.txt
```

---

## 📞 Need Help?

1. Check `HOSTINGER_DEPLOYMENT_GUIDE.md` for detailed steps
2. Review Hostinger error logs: `~/logs/error.log`
3. Contact Hostinger support for server issues
4. Test database connection via phpMyAdmin

---

## 🎯 Post-Deployment Tasks

After successful deployment:

1. **Create Admin User** (if not done during deployment)
2. **Test all features**:
   - Client creation
   - Booking records
   - Payment processing
   - Document uploads
   - Email sending
3. **Configure backups** via Hostinger panel
4. **Setup monitoring** (uptime, errors)
5. **Test on mobile devices**

---

## 🔒 Security Tips

- [ ] Change default admin password immediately
- [ ] Keep SECRET_KEY secure (never commit to Git)
- [ ] Enable automatic database backups
- [ ] Monitor error logs regularly
- [ ] Keep Django and dependencies updated
- [ ] Use strong passwords for all users

---

**Estimated Total Time: 15-20 minutes**

Good luck with your deployment! 🚀
