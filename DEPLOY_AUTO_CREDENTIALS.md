# Deploy Auto-Credentials Feature to PythonAnywhere

## 🚀 Quick Deployment Steps

### Step 1: SSH into PythonAnywhere
```bash
# Go to PythonAnywhere Dashboard → Consoles → Bash
# Or use Web SSH terminal
```

### Step 2: Navigate to Project Directory
```bash
cd ~/agnivridhi
# or wherever your CRM project is located
```

### Step 3: Pull Latest Changes from GitHub
```bash
git pull origin main
```

**Expected Output:**
```
remote: Enumerating objects: 29, done.
remote: Counting objects: 100% (29/29), done.
...
From https://github.com/Utkarsh1506/crm-agnivridhi
   6d065dd..69266b2  main -> main
Updating 6d065dd..69266b2
Fast-forward
 accounts/urls.py                              |   2 +
 accounts/views.py                             |  19 +-
 clients/admin.py                              |  48 +++-
 clients/apps.py                               |   3 +
 clients/models.py                             |  80 +++++++
 clients/signals.py                            |  28 +++
 clients/migrations/0004_clientcredential.py   |  35 +++
 templates/dashboards/owner_dashboard.html     |  58 +++++
 AUTO_CREDENTIALS_FEATURE.md                   | 400 ++++++++++++++++++++++++++
 test_credential_generation.py                 | 115 ++++++++
 10 files changed, 637 insertions(+), 2 deletions(-)
```

### Step 4: Activate Virtual Environment
```bash
source venv/bin/activate
# or
workon your-virtualenv-name
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

**Expected Output:**
```
Migrations for 'clients':
  clients/migrations/0004_clientcredential.py
    - Create model ClientCredential
    
Operations to perform:
  Apply all migrations: accounts, activity_logs, admin, applications, auth, bookings, clients, contenttypes, documents, edit_requests, notifications, payments, schemes, sessions, tracking
Running migrations:
  Applying clients.0004_clientcredential... OK
```

### Step 6: Collect Static Files (if needed)
```bash
python manage.py collectstatic --noinput
```

### Step 7: Reload Web App
```bash
# Option 1: Via Web Interface
# Go to PythonAnywhere Dashboard → Web → Click "Reload" button

# Option 2: Via Command Line (if you have the API)
touch /var/www/your_username_pythonanywhere_com_wsgi.py
```

### Step 8: Verify Deployment
1. Go to: `https://your-username.pythonanywhere.com/admin/`
2. Login as admin
3. Navigate to: **Clients → Client credentials**
4. Should see the new model registered

5. Go to: `https://your-username.pythonanywhere.com/dashboard/owner/`
6. Login as owner/admin
7. If there are no unsent credentials, the section won't show (that's correct)

## ✅ Test the Feature

### Option A: Create Test Client via Django Admin
1. Login to Django Admin: `/admin/`
2. Go to **Accounts → Users**
3. Click **Add User**
   - Username: `testclient_prod`
   - Password: `TempPass123`
   - Role: `CLIENT`
   - Save

4. Go to **Clients → Clients**
5. Click **Add Client**
   - Fill in all required fields:
     - Company name: "Test Company Production"
     - Business type: Choose any
     - Sector: Choose any
     - Company age: 2
     - Contact person: "Test Person"
     - Contact email: "test@test.com"
     - Contact phone: "9876543210"
     - Address fields (all required)
     - Annual turnover: 1000000
     - Funding required: 500000
     - User: Select `testclient_prod` (the user you just created)
     - Assigned sales: Select any sales employee
   - Save

6. Go to Owner Dashboard: `/dashboard/owner/`
7. You should see the red credentials card with the auto-generated password!

### Option B: Use Existing Test Script
```bash
# In PythonAnywhere bash console
cd ~/agnivridhi
source venv/bin/activate
python test_credential_generation.py
```

**Expected Output:**
```
============================================================
Testing Client Credential Auto-Generation
============================================================

0. Cleaning up existing test data...
✓ Cleaned up existing test data
✓ Using sales user: sales9

1. Creating client user account...
✓ Created user: testclient123

2. Creating client profile...
✓ Created client: Test Company Auto Credentials (ID: CLI-20251113-XXXX)

3. Checking if credentials were auto-generated...
✓ Credentials were auto-generated!

============================================================
GENERATED CREDENTIALS:
============================================================
  Company:  Test Company Auto Credentials
  Username: testclient123
  Email:    testclient123@test.com
  Password: [Random 12-char password]
  Created:  2025-11-13 XX:XX:XX
  Is Sent:  False
============================================================

4. Verifying password was set on user account...
✓ Password was successfully set on user account!

============================================================
TEST COMPLETED SUCCESSFULLY!
============================================================
```

## 🔍 Troubleshooting

### Issue 1: Migration Already Applied
**Error:** `No migrations to apply`

**Solution:** This is fine! It means migrations are already up to date.

### Issue 2: Signal Not Firing
**Symptom:** Client created but no ClientCredential record

**Check:**
1. Verify signal is imported in `clients/apps.py`:
   ```python
   def ready(self):
       import clients.signals
   ```

2. Restart the web app:
   - Go to Web tab → Click Reload

3. Check if client has a user account:
   ```python
   python manage.py shell
   >>> from clients.models import Client
   >>> c = Client.objects.last()
   >>> print(c.user)  # Should not be None
   ```

### Issue 3: Permission Denied on Owner Dashboard
**Symptom:** Can't access `/dashboard/owner/`

**Solution:**
```python
# In Django shell
python manage.py shell

from accounts.models import User
owner = User.objects.get(username='owner')
owner.is_owner = True  # or ensure role='OWNER'
owner.save()
```

### Issue 4: Template Not Found
**Symptom:** `TemplateDoesNotExist: dashboards/owner_dashboard.html`

**Solution:**
```bash
# Ensure templates are in correct location
ls templates/dashboards/owner_dashboard.html

# If missing, pull again from git
git pull origin main

# Reload web app
```

## 📊 Verify Database Changes

```bash
python manage.py dbshell
```

### SQLite (local):
```sql
.tables  -- Should show clients_clientcredential
.schema clients_clientcredential
SELECT * FROM clients_clientcredential;
```

### MySQL (production):
```sql
SHOW TABLES LIKE '%credential%';
DESCRIBE clients_clientcredential;
SELECT * FROM clients_clientcredential;
```

## 🎉 Success Indicators

- ✅ Migration applied successfully
- ✅ New table `clients_clientcredential` exists in database
- ✅ ClientCredential appears in Django Admin
- ✅ Owner Dashboard shows credentials card (when credentials exist)
- ✅ Test client creation generates credentials automatically
- ✅ "Mark as Sent" button works and removes credential from display
- ✅ Copy button copies password to clipboard

## 📝 Post-Deployment Checklist

- [ ] Migration applied: `clients.0004_clientcredential`
- [ ] Web app reloaded
- [ ] Test client created successfully
- [ ] Credentials auto-generated
- [ ] Owner Dashboard displays credentials
- [ ] Copy button works
- [ ] Mark as Sent functionality works
- [ ] Django Admin shows ClientCredential model
- [ ] No errors in error log
- [ ] Documented production URL for Owner

## 🔗 Important URLs

### Production URLs (Update with your domain)
- **Owner Dashboard**: `https://your-app.pythonanywhere.com/dashboard/owner/`
- **Django Admin**: `https://your-app.pythonanywhere.com/admin/`
- **Client Credentials Admin**: `https://your-app.pythonanywhere.com/admin/clients/clientcredential/`

### Owner Credentials
- **Username**: `owner` (or `admin` with is_owner=True)
- **Password**: [Your owner password]

## 🐛 Debugging Commands

### Check if signal is connected:
```python
python manage.py shell

from django.db.models.signals import post_save
from clients.models import Client

# Show all signal receivers for Client post_save
print(post_save.receivers)
```

### Check recent credentials:
```python
python manage.py shell

from clients.models import ClientCredential

# Show all credentials
for cred in ClientCredential.objects.all():
    print(f"{cred.client.company_name}: {cred.username} / {cred.plain_password}")
```

### Manual credential creation (if signal fails):
```python
python manage.py shell

from clients.models import Client, ClientCredential
import secrets
import string

client = Client.objects.last()
password = ''.join(secrets.choice(string.ascii_letters + string.digits + "@#$%") for _ in range(12))

ClientCredential.objects.create(
    client=client,
    username=client.user.username,
    email=client.user.email,
    plain_password=password,
    created_by=client.created_by
)
```

## 📞 Support

If you encounter any issues:
1. Check PythonAnywhere error log: Web → Log files → Error log
2. Check Django shell for errors
3. Verify all files were pulled from git
4. Ensure web app was reloaded
5. Check browser console for JavaScript errors (F12)

## 🎯 Expected Behavior

### When Client is Created:
1. Sales/Admin creates client with user account
2. Signal fires automatically
3. Random password generated (12 characters)
4. User password updated
5. ClientCredential record created
6. Owner sees credentials on dashboard

### When Owner Views Dashboard:
1. Red alert card appears (if unsent credentials exist)
2. Table shows: Company, Username, Email, Password
3. Copy button copies password
4. Mark as Sent button visible

### When Marked as Sent:
1. is_sent = True
2. sent_at = current timestamp
3. sent_by = current user
4. Credential disappears from dashboard
5. Still visible in Django Admin

---

**Deployment Date**: November 13, 2025  
**Git Commit**: `69266b2`  
**Feature**: Auto-Generated Client Credentials  
**Status**: Ready for Production ✅
