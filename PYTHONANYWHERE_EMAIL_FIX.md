# PythonAnywhere Email Configuration Fix

## Problem
Emails are not being sent on PythonAnywhere deployment, showing error:
"Could not send email to vharadharajharshitha@gmail.com. Please verify SMTP settings and try again."

## Root Causes & Solutions

### Issue 1: PythonAnywhere SMTP Port Restrictions
**Problem:** Free PythonAnywhere accounts block outbound SMTP on common ports (25, 465, 587, 2525).

**Solutions:**
1. **Upgrade to Paid Account** (Recommended)
   - Paid accounts have unrestricted SMTP access
   - Can use Hostinger SMTP directly

2. **Use PythonAnywhere's Email Whitelist** (For Paid Accounts)
   - Go to: PythonAnywhere Dashboard → Account → Email
   - Add `smtp.hostinger.com` to whitelist

3. **Alternative: Use Gmail SMTP** (Works on Free Accounts)
   - Gmail SMTP is whitelisted even on free accounts
   - Update settings to use Gmail

### Issue 2: Environment Variables Not Set
**Problem:** Production environment variables may not be configured on PythonAnywhere.

**Solution:**
Add to your PythonAnywhere WSGI file (`/var/www/<username>_pythonanywhere_com_wsgi.py`):

```python
import os

# Email Configuration for Production
os.environ['EMAIL_BACKEND'] = 'django.core.mail.backends.smtp.EmailBackend'
os.environ['EMAIL_HOST'] = 'smtp.hostinger.com'
os.environ['EMAIL_PORT'] = '587'
os.environ['EMAIL_USE_TLS'] = 'True'
os.environ['EMAIL_HOST_USER'] = 'noreply@agnivridhiindia.com'
os.environ['EMAIL_HOST_PASSWORD'] = 'NoReply@121'
os.environ['DEFAULT_FROM_EMAIL'] = 'Agnivridhi CRM <noreply@agnivridhiindia.com>'
```

## Step-by-Step Fix for PythonAnywhere

### Option A: Use Gmail SMTP (Works on Free Accounts)

1. **Go to PythonAnywhere Dashboard → Web**
2. **Click on WSGI configuration file**
3. **Add these lines at the top** (after imports):

```python
import os

# Use Gmail SMTP (whitelisted on PythonAnywhere)
os.environ['EMAIL_BACKEND'] = 'django.core.mail.backends.smtp.EmailBackend'
os.environ['EMAIL_HOST'] = 'smtp.gmail.com'
os.environ['EMAIL_PORT'] = '587'
os.environ['EMAIL_USE_TLS'] = 'True'
os.environ['EMAIL_HOST_USER'] = 'your-gmail@gmail.com'  # Change this
os.environ['EMAIL_HOST_PASSWORD'] = 'your-app-password'  # Use App Password
os.environ['DEFAULT_FROM_EMAIL'] = 'Agnivridhi CRM <your-gmail@gmail.com>'
```

4. **Setup Gmail App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Generate a new App Password for "Mail"
   - Use that password in EMAIL_HOST_PASSWORD

5. **Reload your web app** in PythonAnywhere

### Option B: Keep Hostinger SMTP (Paid Accounts Only)

1. **Upgrade to Paid PythonAnywhere Account**
2. **Whitelist Hostinger SMTP:**
   - Dashboard → Account → Email
   - Add `smtp.hostinger.com` to whitelist
3. **Reload web app**

### Option C: Use SendGrid/Mailgun (Free Tier Available)

1. **Sign up for SendGrid** (free 100 emails/day) or Mailgun
2. **Get API key or SMTP credentials**
3. **Update WSGI file** with SendGrid/Mailgun SMTP settings
4. **Reload web app**

## Test Email After Changes

SSH into PythonAnywhere console and run:

```bash
cd ~/agnivridhicrm
source venv/bin/activate
python manage.py shell
```

Then in Python shell:
```python
from django.core.mail import send_mail
from django.conf import settings

print("SMTP Settings:")
print(f"Backend: {settings.EMAIL_BACKEND}")
print(f"Host: {settings.EMAIL_HOST}")
print(f"Port: {settings.EMAIL_PORT}")
print(f"TLS: {settings.EMAIL_USE_TLS}")

# Send test email
send_mail(
    'Test from PythonAnywhere',
    'This is a test email.',
    settings.DEFAULT_FROM_EMAIL,
    ['vharadharajharshitha@gmail.com'],
    fail_silently=False,
)
print("Email sent successfully!")
```

## Check Error Logs

View error logs on PythonAnywhere:
- Dashboard → Web → Error log
- Look for specific SMTP error messages

## Common SMTP Errors on PythonAnywhere

1. **SMTPConnectError**: Port 587 is blocked → Use Gmail or upgrade account
2. **SMTPAuthenticationError**: Wrong credentials → Verify username/password
3. **SMTPException: timed out**: Firewall blocking → Use whitelisted SMTP provider
4. **Connection refused**: SMTP server not accessible → Check host/port

## Recommended Solution

**For Production: Use SendGrid or Mailgun**
- More reliable than shared SMTP servers
- Better deliverability
- Free tier sufficient for most CRMs
- Works on free PythonAnywhere accounts

### SendGrid Setup Example:
```python
os.environ['EMAIL_BACKEND'] = 'django.core.mail.backends.smtp.EmailBackend'
os.environ['EMAIL_HOST'] = 'smtp.sendgrid.net'
os.environ['EMAIL_PORT'] = '587'
os.environ['EMAIL_USE_TLS'] = 'True'
os.environ['EMAIL_HOST_USER'] = 'apikey'
os.environ['EMAIL_HOST_PASSWORD'] = 'your-sendgrid-api-key'
os.environ['DEFAULT_FROM_EMAIL'] = 'noreply@agnivridhiindia.com'
```

## After Making Changes

1. **Push code to GitHub** (if using Git deployment)
2. **Pull changes on PythonAnywhere**
3. **Update WSGI file** with environment variables
4. **Reload web app**
5. **Test email sending**

## Support

If issues persist after trying these solutions:
1. Check PythonAnywhere error logs
2. Test SMTP from PythonAnywhere console
3. Contact PythonAnywhere support about SMTP access
