# SendGrid Setup for Agnivridhi CRM - Step by Step

## Part 1: Create SendGrid Account (2 minutes)

### Step 1: Sign Up
1. Go to: https://signup.sendgrid.com/
2. Fill in:
   - Email: Your email
   - Password: Create strong password
   - Check "I'm not a robot"
3. Click "Create Account"

### Step 2: Verify Email
1. Check your email inbox
2. Click verification link from SendGrid
3. Complete profile:
   - First Name: Utkarsh (or your name)
   - Last Name: Choudhary
   - Company: Agnivridhi India
   - Website: https://agnivridhiindia.com

### Step 3: Tell them about your use
1. Role: Developer
2. Why using SendGrid: "Transactional emails for CRM"
3. How many emails: "100-1000 per month"
4. Complete setup

---

## Part 2: Get API Key (1 minute)

### Step 1: Go to API Keys
1. After login, in left sidebar:
   - Click "Settings" (gear icon at bottom)
   - Click "API Keys"

2. Or direct link: https://app.sendgrid.com/settings/api_keys

### Step 2: Create API Key
1. Click blue "Create API Key" button (top right)
2. API Key Name: `Agnivridhi CRM Production`
3. API Key Permissions: 
   - Choose "Full Access" (recommended)
   - Or "Restricted Access" → Check only "Mail Send"
4. Click "Create & View"

### Step 3: Copy API Key
1. SendGrid shows your API key (starts with `SG.`)
2. **IMPORTANT**: Copy this NOW - you won't see it again!
3. Example: `SG.abcd1234efgh5678ijkl9012mnop3456`
4. Keep it safe temporarily (you'll paste it in next step)

---

## Part 3: Update PythonAnywhere (2 minutes)

### Step 1: Open WSGI File
1. Go to: https://www.pythonanywhere.com/
2. Click "Web" tab
3. Scroll to "Code" section
4. Click on WSGI configuration file link:
   `/var/www/agnivridhicrm_pythonanywhere_com_wsgi.py`

### Step 2: Replace Content
Copy this ENTIRE code and paste it into your WSGI file:

```python
import os
import sys

USERNAME = 'agnivridhicrm'  # Your PythonAnywhere username
PROJECT_NAME = 'crm-agnivridhi'

# Add project to path
project_path = f'/home/{USERNAME}/{PROJECT_NAME}'
if project_path not in sys.path:
    sys.path.append(project_path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'agnivridhi_crm.settings'

# Email Configuration - SendGrid SMTP
os.environ['EMAIL_BACKEND'] = 'django.core.mail.backends.smtp.EmailBackend'
os.environ['EMAIL_HOST'] = 'smtp.sendgrid.net'
os.environ['EMAIL_PORT'] = '587'
os.environ['EMAIL_USE_TLS'] = 'True'
os.environ['EMAIL_HOST_USER'] = 'apikey'  # Do NOT change this
os.environ['EMAIL_HOST_PASSWORD'] = 'PASTE_YOUR_API_KEY_HERE'  # ← PASTE HERE
os.environ['DEFAULT_FROM_EMAIL'] = 'Agnivridhi CRM <noreply@agnivridhiindia.com>'

# Optional: Load .env file if it exists
from pathlib import Path
env_path = Path(f'/home/{USERNAME}/{PROJECT_NAME}/.env')
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 3: Paste API Key
1. Find line: `os.environ['EMAIL_HOST_PASSWORD'] = 'PASTE_YOUR_API_KEY_HERE'`
2. Replace `PASTE_YOUR_API_KEY_HERE` with your actual SendGrid API key
3. Should look like: `os.environ['EMAIL_HOST_PASSWORD'] = 'SG.abcd1234...'`

### Step 4: Save
1. Click green "Save" button at top
2. File is saved!

---

## Part 4: Reload Web App (30 seconds)

### Step 1: Reload
1. Go back to "Web" tab
2. Click big green "Reload" button
3. Wait for "Reloaded!" message

### Step 2: Done! 
Your CRM is now using SendGrid for emails! 🎉

---

## Part 5: Test Email (1 minute)

### Option 1: Create a Test Client
1. Go to your CRM: https://agnivridhicrm.pythonanywhere.com
2. Login as Sales/Admin
3. Create a new client with email: vharadharajharshitha@gmail.com
4. Check if email arrives!

### Option 2: Test via Console
1. PythonAnywhere → Consoles → Bash
2. Run:
```bash
cd ~/crm-agnivridhi
python manage.py shell
```

3. In Python shell:
```python
from django.core.mail import send_mail
from django.conf import settings

print("Testing SendGrid...")
print(f"Host: {settings.EMAIL_HOST}")
print(f"User: {settings.EMAIL_HOST_USER}")

send_mail(
    'SendGrid Test - Agnivridhi CRM',
    'SendGrid SMTP is working perfectly!',
    settings.DEFAULT_FROM_EMAIL,
    ['vharadharajharshitha@gmail.com'],
    fail_silently=False,
)
print("✅ Email sent via SendGrid!")
```

---

## Part 6: Verify Domain (Optional but Recommended)

### Why verify domain?
- Emails sent from noreply@agnivridhiindia.com will be trusted
- Won't go to spam
- Shows professional sender

### Steps:
1. SendGrid → Settings → Sender Authentication
2. Click "Verify a Domain"
3. Enter: agnivridhiindia.com
4. SendGrid gives you DNS records
5. Add these records to your domain registrar (Hostinger/GoDaddy/etc)
6. Wait 24-48 hours for verification

### DNS Records (SendGrid will show exact values):
- **CNAME Record 1**: em1234.agnivridhiindia.com → u1234567.wl.sendgrid.net
- **CNAME Record 2**: s1._domainkey.agnivridhiindia.com → s1.domainkey.u1234567.wl.sendgrid.net
- **CNAME Record 3**: s2._domainkey.agnivridhiindia.com → s2.domainkey.u1234567.wl.sendgrid.net

---

## 🎯 Quick Checklist

- [ ] Sign up for SendGrid
- [ ] Verify email
- [ ] Create API Key
- [ ] Copy API Key (starts with SG.)
- [ ] Update WSGI file on PythonAnywhere
- [ ] Paste API Key in EMAIL_HOST_PASSWORD
- [ ] Save WSGI file
- [ ] Reload web app
- [ ] Test email
- [ ] ✅ Emails working!

---

## 🔧 Troubleshooting

### Error: "Unable to login"
**Problem**: API key is wrong or has wrong format
**Solution**: 
- Make sure it starts with `SG.`
- No extra spaces
- Regenerate API key if needed

### Error: "Connection refused"
**Problem**: WSGI file not saved or app not reloaded
**Solution**:
- Save WSGI file again
- Reload web app
- Wait 30 seconds

### Error: "Bad Request"
**Problem**: EMAIL_HOST_USER is not exactly "apikey"
**Solution**:
- Must be literally `'apikey'` (lowercase, no spaces)
- Do NOT put your email or username

### Emails going to spam
**Solution**:
1. Ask recipient to mark as "Not Spam"
2. Verify your domain (Part 6 above)
3. Add SPF record to DNS
4. Warm up the sending (start with few emails)

---

## 📊 SendGrid Dashboard

After sending emails, check:
- **Dashboard → Stats**: See delivery rates
- **Activity**: See individual email status
- **Suppressions**: See bounced/blocked emails

---

## 💰 Pricing (When You Scale)

| Plan | Emails/Month | Price | Good For |
|------|-------------|-------|----------|
| **Free** | 100/day (~3K/month) | $0 | Starting up ✅ |
| Essentials | 50,000 | $20/mo | Growing |
| Pro | 100,000+ | $90/mo | Enterprise |

---

## 🎉 All Done!

Your CRM now sends professional emails via SendGrid!

**What changed:**
- ❌ Before: Emails blocked on PythonAnywhere
- ✅ Now: Professional emails from noreply@agnivridhiindia.com
- ✅ 100 emails/day capacity
- ✅ No spam issues
- ✅ Professional deliverability

**Next Steps:**
1. Test by creating a client
2. Monitor SendGrid dashboard
3. Verify your domain for best results
4. Scale up when needed (cheap to upgrade)

Need help with any step? Let me know!
