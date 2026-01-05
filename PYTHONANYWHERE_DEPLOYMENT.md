# 🚀 PythonAnywhere Deployment Guide

**Date**: January 5, 2026  
**Project**: Agnivridhi CRM - Employee System Update  
**Repository**: https://github.com/Utkarsh1506/crm-agnivridhi  
**Status**: ✅ Changes Pushed to Main Branch  

---

## ✅ Git Push Complete

```
Commit: 84d432a - "Feat: Add Employee ID System with 4-digit format..."
Branch: main
Remote: origin (GitHub)
Files Changed: 50
Insertions: 11,222+
Status: ✅ Successfully pushed
```

---

## 🚀 PythonAnywhere Deployment Steps

### Prerequisites
- ✅ Git repository linked to PythonAnywhere
- ✅ Virtual environment set up
- ✅ Database (PostgreSQL) running

---

## Step 1: SSH into PythonAnywhere

Log into your PythonAnywhere account:

```bash
# From PythonAnywhere Bash Console:
# Go to: https://www.pythonanywhere.com/
# Click: "Bash console" on your account
```

Or via SSH (if you have SSH access):
```bash
ssh username@username.pythonanywhere.com
```

---

## Step 2: Navigate to Your Project

```bash
cd /home/YOUR_USERNAME/crm-agnivridhi
```

Replace `YOUR_USERNAME` with your actual PythonAnywhere username.

---

## Step 3: Pull Latest Changes from GitHub

```bash
git pull origin main
```

**Expected Output:**
```
Updating f4ab878..84d432a
Fast-forward
 CHANGES_SUMMARY.md | ...
 employees/ | ...
 (50 files changed, +11222 insertions)
```

---

## Step 4: Activate Virtual Environment

```bash
source venv/bin/activate
```

Or if your virtual environment has a different name:
```bash
source /home/YOUR_USERNAME/.virtualenvs/YOUR_VENV_NAME/bin/activate
```

---

## Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed qrcode-7.4.2
...
```

---

## Step 6: Run Database Migrations

```bash
python manage.py migrate employees
```

**Expected Output:**
```
Operations to perform:
  Apply all migrations: employees
Running migrations:
  Applying employees.0001_initial... OK
```

---

## Step 7: Seed the 17 Employees

```bash
python manage.py seed_agnivridhi_employees
```

**Expected Output:**
```
Starting Agnivridhi employee data seeding...
✓ Created 0101 - Rahul Kumar Singh (Sales)
✓ Created 0102 - Urvashi Nandan Srivastava (Marketing)
... (15 more employees)
✓ Successfully created 17 employees!
```

---

## Step 8: Collect Static Files (If Needed)

If you're running a production server:

```bash
python manage.py collectstatic --noinput
```

---

## Step 9: Reload Web App

In PythonAnywhere Web Console:

1. Go to **Web** tab
2. Find your app (e.g., `yourname.pythonanywhere.com`)
3. Click **Reload**

Or reload via bash:
```bash
touch /var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py
```

---

## Step 10: Verify Deployment

### Test 1: Check Admin Interface
```bash
# In bash console:
python manage.py shell

>>> from employees.models import Employee
>>> print(f"Total employees: {Employee.objects.count()}")
17
>>> emp = Employee.objects.get(employee_id='0101')
>>> print(f"{emp.employee_id} - {emp.full_name}")
0101 - Rahul Kumar Singh
>>> exit()
```

### Test 2: Visit Public Verification Page

Open in browser:
```
https://YOUR_USERNAME.pythonanywhere.com/employees/verify/0101/
```

You should see Rahul Kumar Singh's details without login.

### Test 3: Check Admin Panel

```
https://YOUR_USERNAME.pythonanywhere.com/admin/employees/employee/
```

You should see all 17 employees listed.

---

## Complete Bash Script (Copy-Paste Ready)

```bash
#!/bin/bash

echo "=== Deploying Employee System Update to PythonAnywhere ==="

# Navigate to project
cd /home/YOUR_USERNAME/crm-agnivridhi

echo "1. Pulling latest changes..."
git pull origin main

# Activate virtual environment
echo "2. Activating virtual environment..."
source venv/bin/activate
# Or: source /home/YOUR_USERNAME/.virtualenvs/YOUR_VENV_NAME/bin/activate

echo "3. Installing dependencies..."
pip install -r requirements.txt

echo "4. Running migrations..."
python manage.py migrate employees

echo "5. Seeding 17 employees..."
python manage.py seed_agnivridhi_employees

echo "6. Collecting static files..."
python manage.py collectstatic --noinput

echo "7. Verifying installation..."
python manage.py shell << EOF
from employees.models import Employee
print(f"✓ Total employees: {Employee.objects.count()}")
print("✓ Deployment successful!")
exit()
EOF

echo "=== Reloading web app in Web console ==="
touch /var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py

echo "✅ DEPLOYMENT COMPLETE!"
echo ""
echo "Visit: https://YOUR_USERNAME.pythonanywhere.com/employees/verify/0101/"
```

Replace `YOUR_USERNAME` with your actual username before running.

---

## PythonAnywhere Web Console Steps

If using PythonAnywhere Web Console instead of SSH:

### Step A: Open Bash Console
1. Log in to https://pythonanywhere.com
2. Go to **Consoles** tab
3. Click **$ Bash**

### Step B: Run Commands in Console

```bash
# 1. Navigate to project
cd crm-agnivridhi

# 2. Pull changes
git pull origin main

# 3. Activate venv
workon agnivridhi  # or your venv name
# or: source venv/bin/activate

# 4. Install
pip install -r requirements.txt

# 5. Migrate
python manage.py migrate employees

# 6. Seed
python manage.py seed_agnivridhi_employees
```

### Step C: Reload Web App

1. Go to **Web** tab
2. Find your web app (e.g., `yourname.pythonanywhere.com`)
3. Click green **Reload** button

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'employees'"

**Solution:**
```bash
# Check if employees is in INSTALLED_APPS
python manage.py shell
>>> from django.conf import settings
>>> 'employees' in settings.INSTALLED_APPS
True  # Should return True

# If not, add it to settings.py in INSTALLED_APPS
```

### Issue: Migration errors

**Solution:**
```bash
# Check migration status
python manage.py showmigrations employees

# If stuck, reset migrations (development only!):
python manage.py migrate employees zero  # Unapply all
python manage.py migrate employees       # Reapply
```

### Issue: "Permission denied" for git pull

**Solution:**
```bash
# Check git configuration
git config --list | grep url

# If using HTTPS, you might need to use a Personal Access Token
# Set it in git: git config credential.helper store
```

### Issue: "Static files not found" (404 errors)

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check file permissions
ls -la /var/www/YOUR_USERNAME_pythonanywhere_com_static/
```

### Issue: "Database connection refused"

**Solution:**
```bash
# Check database configuration in settings.py
python manage.py shell
>>> from django.db import connection
>>> connection.ensure_connection()  # Should not raise error

# If using PostgreSQL, verify credentials in .env or settings
```

---

## Verification Checklist

After deployment, verify:

- [ ] `git pull origin main` completed successfully
- [ ] All dependencies installed (pip install output shows success)
- [ ] Migrations applied (`migrate employees` shows OK)
- [ ] 17 employees seeded (`seed_agnivridhi_employees` shows ✓)
- [ ] Static files collected
- [ ] Web app reloaded
- [ ] Can access admin: https://yoursite.pythonanywhere.com/admin/
- [ ] Can verify employee: https://yoursite.pythonanywhere.com/employees/verify/0101/
- [ ] Django shell shows 17 employees
- [ ] No errors in error logs

---

## Post-Deployment Steps

### 1. Monitor Error Logs
```bash
# SSH into PythonAnywhere and check:
tail -f /var/www/YOUR_USERNAME_pythonanywhere_com_error.log
tail -f /var/www/YOUR_USERNAME_pythonanywhere_com_access.log
```

Or in PythonAnywhere Web console:
1. Go to **Web** tab
2. Click your app name
3. Scroll down to view error/access logs

### 2. Check Database

```bash
python manage.py dbshell

-- Check employee count
SELECT COUNT(*) FROM employees_employee;

-- Check specific employee
SELECT id, employee_id, full_name FROM employees_employee WHERE employee_id = '0101';

-- Check sequence
SELECT last_sequence_number FROM employees_employeeidsequence;
```

### 3. Test Features

```bash
# Test QR code generation
python manage.py shell
>>> from employees.models import Employee
>>> emp = Employee.objects.get(employee_id='0101')
>>> print(f"Has QR: {bool(emp.qr_code)}")
True

# Test verification token
>>> print(f"Has Token: {bool(emp.verification_token)}")
True
```

### 4. Monitor Users

1. Go to PythonAnywhere **Web** tab
2. Check traffic and performance metrics
3. Review access logs for verification endpoint

---

## Rollback (If Needed)

If something goes wrong and you need to revert:

```bash
# Go to previous commit
git reset --hard f4ab878

# Or checkout a previous tag
git tag  # List all tags
git checkout <tag-name>

# Then reload web app
```

---

## Environment Variables Check

Ensure your `.env` file is set up correctly on PythonAnywhere:

```bash
# In PythonAnywhere bash:
cat .env

# Should contain:
SECRET_KEY=your_secret_key
DEBUG=False  # Important for production!
ALLOWED_HOSTS=your_domain.pythonanywhere.com
DATABASE_URL=your_db_connection_string
```

If missing, update `.env`:
```bash
nano .env
# Add your configuration
# Press Ctrl+O to save, Ctrl+X to exit
```

---

## Performance Optimization

After deployment:

1. **Enable Caching**
   ```bash
   # In settings.py, ensure caching is configured
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
       }
   }
   ```

2. **Compress Static Files**
   ```bash
   python manage.py compress --force-inline
   ```

3. **Database Indexing**
   - The migration includes indexes for `employee_id`, `uuid`, and other key fields
   - Verification should be fast

---

## Support Resources

### In PythonAnywhere

1. **Help/Documentation**: https://www.pythonanywhere.com/help/
2. **Forums**: https://www.pythonanywhere.com/forums/
3. **Contact Support**: In your account dashboard

### For This Project

1. **Deployment Guide**: DEPLOYMENT_COMMANDS.md
2. **Setup Guide**: EMPLOYEE_ID_SETUP.md
3. **Quick Reference**: EMPLOYEE_ID_QUICK_REFERENCE.md

---

## Quick Summary

```
DEPLOYMENT STEPS:
1. SSH/Bash console → navigate to project
2. git pull origin main
3. Activate venv
4. pip install -r requirements.txt
5. python manage.py migrate employees
6. python manage.py seed_agnivridhi_employees
7. python manage.py collectstatic --noinput
8. Reload web app in PythonAnywhere Web console
9. Verify at /admin/ and /employees/verify/0101/

TOTAL TIME: ~5-10 minutes
```

---

## Success Indicators

✅ **You're successfully deployed when:**

- 17 employees appear in admin
- `/employees/verify/0101/` shows Rahul Kumar Singh
- No 500 errors in logs
- QR codes generated for each employee
- Rate limiting works (11th request blocked)
- Public verification page accessible without login

---

**Status**: ✅ **READY TO DEPLOY**

All changes are pushed to GitHub. Just follow these steps on PythonAnywhere and you'll be live!

---

**Questions?** Check the documentation files in the repository or contact PythonAnywhere support.

**Estimated Deployment Time**: 5-10 minutes  
**Downtime**: Minimal (automatic during reload)  
**Rollback Time**: <1 minute (if needed)
