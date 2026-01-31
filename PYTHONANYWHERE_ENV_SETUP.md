# PythonAnywhere Environment Variables Setup

## Problem Diagnosis
The production logs show:
```
CLERK_SECRET_KEY not configured - Clerk OTP will not work
```

This indicates that the `.env` file is not being loaded on PythonAnywhere. The issue occurs because:
1. `.env` file is NOT committed to git (it's in `.gitignore`)
2. PythonAnywhere clones the git repository, so `.env` doesn't exist there
3. Django's `load_dotenv()` fails silently when `.env` is missing

## Solution: Three Methods (Use One)

### Method 1: Web Interface (SIMPLEST) ⭐ RECOMMENDED
Go to: https://www.pythonanywhere.com/user/agnivridhicrm/webapps/

1. **Find your web app:** `agnivridhicrm.pythonanywhere.com`
2. **Scroll to "Web app security"** section
3. **Look for "Environment variables"** or similar setting
4. **Add these variables:**

```
CLERK_SECRET_KEY=sk_test_Uzd7yFdLxr5B13dlOktPvYp5hST63dS0l3bEsuMyKz
CLERK_PUBLIC_KEY=pk_test_dGVuZGVyLXNlYXNuYWlsLTk5LmNsZXJrLmFjY291bnRzLmRldiQ
SECRET_KEY=your-django-secret-key-here
DEBUG=False
ALLOWED_HOSTS=agnivridhicrm.pythonanywhere.com
```

5. **Click Reload** web app button

---

### Method 2: Manual .env File in Production
Via **PythonAnywhere Bash Console:**

```bash
cd /home/agnivridhicrm/crm-agnivridhi

# Create .env file
cat > .env << 'EOF'
DEBUG=False
ALLOWED_HOSTS=agnivridhicrm.pythonanywhere.com
SECRET_KEY=your-django-secret-key
CLERK_SECRET_KEY=sk_test_Uzd7yFdLxr5B13dlOktPvYp5hST63dS0l3bEsuMyKz
CLERK_PUBLIC_KEY=pk_test_dGVuZGVyLXNlYXNuYWlsLTk5LmNsZXJrLmFjY291bnRzLmRldiQ
EOF

# Verify it was created
cat .env

# Set secure permissions
chmod 600 .env
```

---

### Method 3: Settings-Based Configuration (FALLBACK)
Modify `agnivridhi_crm/settings.py` to read from PythonAnywhere environment variables:

```python
# After line: from dotenv import load_dotenv

# Try to load from .env first (development)
load_dotenv(BASE_DIR / '.env')

# Then load from PythonAnywhere environment variables (production)
import os
if not os.getenv('CLERK_SECRET_KEY'):
    # Fall back to settings if needed
    CLERK_SECRET_KEY = os.getenv('CLERK_SECRET_KEY', 'sk_test_')
```

---

## Step-by-Step Fix for Your Production Issue

### 1. Access PythonAnywhere Web App Settings
- **URL:** https://www.pythonanywhere.com/user/agnivridhicrm/webapps/
- **App:** `agnivridhicrm.pythonanywhere.com`

### 2. Set Environment Variables (QUICK FIX)
```
CLERK_SECRET_KEY=sk_test_Uzd7yFdLxr5B13dlOktPvYp5hST63dS0l3bEsuMyKz
CLERK_PUBLIC_KEY=pk_test_dGVuZGVyLXNlYXNuYWlsLTk5LmNsZXJrLmFjY291bnRzLmRldiQ
```

### 3. Reload Web App
Click **"Reload agnivridhicrm.pythonanywhere.com"** button

### 4. Test
Visit: http://agnivridhicrm.pythonanywhere.com/client-login/

You should no longer see:
```
CLERK_SECRET_KEY not configured
```

---

## About the URL Error (`NoReverseMatch`)

The error about `'client_email_login' not found` is **secondary** - it happens because:
1. View tries to load but fails silently
2. Template rendering fails
3. Template tries to reverse URL
4. Reverse fails before the real error is shown

Once CLERK_SECRET_KEY is configured, this should resolve automatically.

---

## Email Configuration (SMTP Network Error)

The error `OSError: [Errno 101] Network is unreachable` for SMTP indicates:

### Option A: Use SendGrid (Recommended for PythonAnywhere)
```python
# In settings.py
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = 'your-sendgrid-api-key'
DEFAULT_FROM_EMAIL = 'noreply@agnivridhi.com'
```

### Option B: Use Clerk's Built-in Email
Clerk handles sending OTP emails directly - you don't need SMTP config! The error is from Django trying to send something else (probably password reset emails).

### Option C: PythonAnywhere Email (May not work from free tier)
Contact PythonAnywhere support to enable SMTP for your account.

---

## Verification Checklist

After applying the fix:

- [ ] Environment variables set on PythonAnywhere
- [ ] Web app reloaded
- [ ] `/client-login/` page loads without "not configured" errors
- [ ] OTP form displays correctly
- [ ] Email entry works (no reverse URL errors)
- [ ] OTP emails arrive when form submitted

---

## For Production (Live Keys)

When ready to deploy with live Clerk keys:

```
CLERK_SECRET_KEY=sk_live_YOUR_LIVE_SECRET_KEY
CLERK_PUBLIC_KEY=pk_live_YOUR_LIVE_PUBLIC_KEY
DEBUG=False
```

Then reload web app.

---

## Quick Bash Test

To verify environment variables are loaded:

```bash
cd /home/agnivridhicrm/crm-agnivridhi
python -c "
import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path('.env'))
print('CLERK_SECRET_KEY:', os.getenv('CLERK_SECRET_KEY'))
print('DEBUG:', os.getenv('DEBUG'))
"
```

---

## Contact PythonAnywhere Support If:
- You can't find where to set environment variables
- The reload button doesn't exist
- Variables still aren't loading after setting them
