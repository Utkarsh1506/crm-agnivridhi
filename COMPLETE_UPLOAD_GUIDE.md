# Complete Upload Guide - Choose Your Method

## Your Server Details
- **Host:** 195.35.44.250
- **Port:** 65002 (SFTP)
- **Username:** u623641178
- **Password:** agnivridhi@CRM121
- **Remote Directory:** /public_html/crm.agnivridhiindia.com

---

## METHOD 1: Python Script Upload (Automated) ⭐ RECOMMENDED

### Step 1: Install paramiko
```powershell
cd C:\Users\Admin\Desktop\agni\CRM
pip install paramiko
```

### Step 2: Run the upload script
```powershell
python upload_to_hostinger.py
```

This will automatically upload all necessary files!

---

## METHOD 2: WinSCP (GUI) - Easiest for Beginners

### Step 1: Download WinSCP
Download from: https://winscp.net/eng/download.php

### Step 2: Open WinSCP and Configure
1. Click "New Site"
2. Fill in:
   - File protocol: **SFTP**
   - Host name: **195.35.44.250**
   - Port number: **65002**
   - User name: **u623641178**
   - Password: **agnivridhi@CRM121**
3. Click "Save" and "Login"

### Step 3: Upload Files
1. Left panel: Navigate to `C:\Users\Admin\Desktop\agni\CRM`
2. Right panel: Navigate to `/public_html/crm.agnivridhiindia.com`
3. Right-click on right panel → "New" → "Directory" → Create `crm.agnivridhiindia.com`
4. Select these items from left panel:
   - manage.py
   - requirements-production.txt
   - passenger_wsgi.py
   - .htaccess
   - .env.production
   - deploy-hostinger.sh
   - All folders (accounts, agnivridhi_crm, applications, etc.)
   
5. Drag and drop to right panel
6. **EXCLUDE:** venv/, __pycache__/, db.sqlite3, .env (local)

---

## METHOD 3: WinSCP Script (Command Line)

### Step 1: Install WinSCP (if not installed)
Download: https://winscp.net/eng/download.php

### Step 2: Run the script
```powershell
cd C:\Users\Admin\Desktop\agni\CRM
"C:\Program Files (x86)\WinSCP\WinSCP.com" /script=upload_winscp.txt
```

Or if WinSCP is in different location:
```powershell
& "C:\Path\To\WinSCP.com" /script=upload_winscp.txt
```

---

## METHOD 4: FileZilla (Alternative GUI)

### Step 1: Download FileZilla
Download: https://filezilla-project.org/download.php?type=client

### Step 2: Configure Site
1. File → Site Manager → New Site
2. Fill in:
   - Protocol: **SFTP**
   - Host: **195.35.44.250**
   - Port: **65002**
   - Logon Type: **Normal**
   - User: **u623641178**
   - Password: **agnivridhi@CRM121**
3. Click "Connect"

### Step 3: Upload Files
1. Local site (left): Navigate to `C:\Users\Admin\Desktop\agni\CRM`
2. Remote site (right): Navigate to `/public_html/crm.agnivridhiindia.com`
3. Select files/folders and drag to right panel

---

## METHOD 5: Manual Interactive SFTP

```powershell
cd C:\Users\Admin\Desktop\agni\CRM
sftp -P 65002 u623641178@195.35.44.250
```

When prompted, enter password: `agnivridhi@CRM121`

Then run these commands:
```bash
mkdir /public_html/crm.agnivridhiindia.com
cd /public_html/crm.agnivridhiindia.com
put manage.py
put requirements-production.txt
put passenger_wsgi.py
put .htaccess
put .env.production
put deploy-hostinger.sh
put export_sqlite_data.py
put import_to_mysql.py
put -r accounts
put -r agnivridhi_crm
put -r applications
put -r bookings
put -r clients
put -r documents
put -r edit_requests
put -r notifications
put -r payments
put -r schemes
put -r activity_logs
put -r templates
put -r static
put -r media
bye
```

---

## WHAT TO UPLOAD (Checklist)

### ✅ Root Files:
- [ ] manage.py
- [ ] requirements-production.txt
- [ ] passenger_wsgi.py
- [ ] .htaccess
- [ ] .env.production
- [ ] deploy-hostinger.sh
- [ ] export_sqlite_data.py
- [ ] import_to_mysql.py

### ✅ Folders:
- [ ] accounts/
- [ ] agnivridhi_crm/
- [ ] applications/
- [ ] bookings/
- [ ] clients/
- [ ] documents/
- [ ] edit_requests/
- [ ] notifications/
- [ ] payments/
- [ ] schemes/
- [ ] activity_logs/
- [ ] templates/
- [ ] static/
- [ ] media/

### ❌ DO NOT UPLOAD:
- ❌ venv/ (will create on server)
- ❌ __pycache__/ (Python cache)
- ❌ *.pyc files
- ❌ db.sqlite3 (local database)
- ❌ .env (your local config)
- ❌ .git/ (git repository)

---

## AFTER UPLOAD: Deployment Steps

### 1. SSH into server
```powershell
ssh -p 65002 u623641178@195.35.44.250
```

### 2. Navigate to project
```bash
cd ~/public_html/crm.agnivridhiindia.com
ls -la  # Verify files are uploaded
```

### 3. Rename environment file
```bash
mv .env.production .env
chmod 600 .env
```

### 4. Run deployment script
```bash
chmod +x deploy-hostinger.sh
./deploy-hostinger.sh
```

Or deploy manually:
```bash
# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements-production.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Set permissions
chmod -R 755 ~/public_html/crm.agnivridhiindia.com

# Restart application
mkdir -p tmp
touch tmp/restart.txt
```

### 5. Test the website
Visit: https://crm.agnivridhiindia.com

---

## Troubleshooting

### "Permission denied" during upload
- Make sure you're using SFTP (not FTP)
- Port must be 65002
- Check username: u623641178
- Check password: agnivridhi@CRM121

### "Connection refused"
- Verify server is accessible: `Test-NetConnection 195.35.44.250 -Port 65002`
- Check if Hostinger SSH/SFTP is enabled in control panel

### Files uploaded but website not working
1. Check if .env.production was renamed to .env
2. Run deployment script
3. Check error logs: `tail -f ~/logs/error.log`
4. Restart Passenger: `touch ~/public_html/crm.agnivridhiindia.com/tmp/restart.txt`

---

## Quick Start - 3 Minutes ⚡

**Fastest method:**
1. `pip install paramiko`
2. `python upload_to_hostinger.py`
3. Wait for upload to complete
4. SSH and run deployment

**Done!** 🎉
