# PythonAnywhere Troubleshooting Guide

## Error Log Analysis

Your production logs revealed three issues. This guide explains what went wrong and how to fix each one.

---

## Issue #1: CLERK_SECRET_KEY Not Configured ❌

### Error Messages
```
CLERK_SECRET_KEY not configured - Clerk OTP will not work
CLERK_SECRET_KEY not configured - attempted to reload from environment
CLERK_SECRET_KEY not configured - checked at send_otp time
```

### What Happened
1. Your code pushed to GitHub without `.env` file (correct - `.env` is in `.gitignore`)
2. PythonAnywhere cloned the repo, but `.env` doesn't exist on the server
3. Django tried to load `.env` during startup but found nothing
4. Clerk API key = empty string
5. OTP authentication breaks

### Root Cause Timeline
```
App Start
  ↓
Load .env from disk
  ↓
.env NOT FOUND (not in git)
  ↓
CLERK_SECRET_KEY = '' (empty)
  ↓
User clicks "Send OTP"
  ↓
Service checks CLERK_SECRET_KEY
  ↓
Empty! Cannot send OTP
  ↓
❌ Error: "OTP service not configured"
```

### The Fix

**Option A: PythonAnywhere Environment Variables (EASIEST)**

1. Go to: https://www.pythonanywhere.com/user/agnivridhicrm/webapps/
2. Click your web app name
3. Scroll to **Environment variables** section
4. Set:
   ```
   CLERK_SECRET_KEY=sk_test_Uzd7yFdLxr5B13dlOktPvYp5hST63dS0l3bEsuMyKz
   CLERK_PUBLIC_KEY=pk_test_dGVuZGVyLXNlYXNuYWlsLTk5LmNsZXJrLmFjY291bnRzLmRldiQ
   ```
5. Click Save/Reload

**Option B: Create .env File on Server**

```bash
# Via PythonAnywhere bash console
cd /home/agnivridhicrm/crm-agnivridhi
cat > .env << 'EOF'
CLERK_SECRET_KEY=sk_test_Uzd7yFdLxr5B13dlOktPvYp5hST63dS0l3bEsuMyKz
CLERK_PUBLIC_KEY=pk_test_dGVuZGVyLXNlYXNuYWlsLTk5LmNsZXJrLmFjY291bnRzLmRldiQ
EOF

# Reload to apply
touch /var/www/agnivridhicrm_pythonanywhere_com_wsgi.py
```

### Verification

After fix, check logs:
```
✅ ClerkOTPService initialized - Key present: True
✅ OTP sent successfully to user@email.com
```

---

## Issue #2: NoReverseMatch URL Error ❌

### Error Message
```
django.urls.exceptions.NoReverseMatch: Reverse for 'client_email_login' not found.
'client_email_login' is not a valid view function or pattern name.
```

### What Happened
1. Request comes in to `/client-login/`
2. View loads: `ClientEmailLoginView`
3. View tries to render template: `client_email_login.html`
4. Template has: `{% url 'accounts:client_email_login' %}`
5. URL reversal works fine in normal cases
6. But service initialization failed silently (no CLERK_SECRET_KEY)
7. Template rendering throws exception before URL is reversed
8. Error displays as URL not found (secondary error message)

### Why It's Secondary
The real issue is #1 (missing CLERK_SECRET_KEY), but Django doesn't show that. Instead, it shows the template error, which appears to be a URL problem. Classic Django error masking.

### The Real Fix
**Fix Issue #1 first.** This error resolves automatically.

### Verification
After fixing Issue #1, visit http://agnivridhicrm.pythonanywhere.com/client-login/

You should see:
- ✅ Email input form loads
- ✅ "Send OTP" button visible
- ✅ No template errors

---

## Issue #3: SMTP Network Error ❌

### Error Message
```
OSError: [Errno 101] Network is unreachable
  File "/usr/lib/python3.10/smtplib.py", line 312, in _get_socket
    return socket.create_connection((host, port), timeout,
```

### What Happened
1. Django tries to send an email (password reset, notifications, etc.)
2. Connects to SMTP server (smtp.hostinger.com)
3. Network connection fails
4. PythonAnywhere free tier doesn't allow outbound SMTP
5. ❌ OSError: Network unreachable

### Why It Happens
- PythonAnywhere free tier blocks SMTP connections
- Prevents spam abuse
- Only accounts with paid hosting or special permission can use SMTP

### The Fix

**Option A: Use SendGrid (Recommended)**

1. **Get SendGrid Account:**
   - Go to: https://sendgrid.com
   - Sign up (free tier available)
   - Create API key with "Mail Send" permission

2. **Install Package:**
   ```bash
   pip install django-sendgrid-v5
   pip freeze > requirements.txt  # Update requirements
   git add requirements.txt
   git commit -m "Add SendGrid support"
   git push origin main
   ```

3. **Configure in settings.py:**
   ```python
   EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
   SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')
   DEFAULT_FROM_EMAIL = 'noreply@agnivridhi.com'
   ```

4. **Set Environment Variable on PythonAnywhere:**
   ```
   SENDGRID_API_KEY=SG.your_sendgrid_api_key_here
   ```

5. **Reload web app**

**Option B: Use Console Backend (Testing Only)**

For testing without actually sending emails:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Emails print to console instead of being sent.

**Option C: Use File Backend (Temporary)**

For development/testing:
```python
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages'  # Emails saved as files
```

### Verification

After setup, send test email:
```bash
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test.',
    'noreply@agnivridhi.com',
    ['test@example.com'],
    fail_silently=False,
)
# Should succeed without network error
```

---

## Complete Fix Summary

### ✅ To-Do Checklist

1. **URGENT - Fix CLERK_SECRET_KEY**
   - [ ] Go to PythonAnywhere web app settings
   - [ ] Add CLERK_SECRET_KEY environment variable
   - [ ] Add CLERK_PUBLIC_KEY environment variable
   - [ ] Click Reload
   - [ ] Test: Visit `/client-login/` - should work

2. **SMTP Email (Optional but Recommended)**
   - [ ] Get SendGrid account
   - [ ] Create API key
   - [ ] Install django-sendgrid-v5
   - [ ] Update settings.py
   - [ ] Set SENDGRID_API_KEY on PythonAnywhere
   - [ ] Test email sending

3. **Verify Logs**
   - [ ] Check `/var/log/agnivridhicrm_pythonanywhere_com_error.log`
   - [ ] Look for: `✅ ClerkOTPService initialized - Key present: True`
   - [ ] No more "CLERK_SECRET_KEY not configured" messages

### 📊 Expected Log Changes

**Before Fix:**
```
CLERK_SECRET_KEY not configured - Clerk OTP will not work
ClerkOTPService initialized - Key present: False
```

**After Fix:**
```
✅ ClerkOTPService initialized successfully - API key loaded (length: 56)
📧 Sending OTP to user@example.com via Clerk API
✅ OTP sent successfully to user@example.com
```

---

## Debugging Commands

### Check Environment Variables Set
```bash
cd /home/agnivridhicrm/crm-agnivridhi
python -c "import os; print('CLERK_SECRET_KEY:', os.getenv('CLERK_SECRET_KEY'))"
```

### View Logs in Real-Time
```bash
tail -f /var/log/agnivridhicrm_pythonanywhere_com_error.log
```

### Test OTP Service Directly
```bash
python manage.py shell

from accounts.clerk_otp_service import clerk_service
result = clerk_service.send_otp('test@example.com')
print(result)
```

### Check Web App Status
```bash
# Via PythonAnywhere bash console
# Check if web app is running
ps aux | grep wsgi
```

---

## When Things Go Wrong

### Problem: Variables Still Not Loaded
**Solution:**
1. Check spelling (case-sensitive: CLERK_SECRET_KEY, not clerk_secret_key)
2. Wait 30 seconds for reload to complete
3. Try Option B (create .env file) instead
4. Contact PythonAnywhere support if still broken

### Problem: OTP Sending Still Fails
**Check:**
1. Is CLERK_SECRET_KEY actually set? (check env variables)
2. Does the API key format look correct? (starts with sk_test_ or sk_live_)
3. Is Clerk API reachable from PythonAnywhere? (may need to check firewall)
4. Check full error in logs

### Problem: Emails Still Failing
**If using SendGrid:**
1. Verify SENDGRID_API_KEY is set
2. Check API key is correct (from SendGrid dashboard)
3. Verify email address is valid
4. Check SendGrid account isn't rate limited

### Problem: Multiple Errors
**Try this order:**
1. Fix CLERK_SECRET_KEY first (blocks /client-login/ page)
2. Then fix SMTP/Email (affects other features)
3. Check logs after each fix
4. Reload web app between fixes

---

## Testing Workflow

### 1. Test OTP Authentication
```
1. Visit http://agnivridhicrm.pythonanywhere.com/client-login/
2. Enter test client email (must be approved client)
3. Click "Send OTP"
4. Check email for OTP code
5. Enter code and click "Verify"
6. Should login successfully
```

### 2. Test Email Sending
```
1. Trigger password reset (if configured)
2. Or use Django shell to send test email
3. Verify email arrives
4. Check no errors in logs
```

### 3. Check Logs
```bash
# SSH into PythonAnywhere
tail -100 /var/log/agnivridhicrm_pythonanywhere_com_error.log

# Look for:
✅ Success messages
❌ Any errors or warnings
⚠️ Configuration issues
```

---

## Quick Reference

| Error | Cause | Fix |
|-------|-------|-----|
| CLERK_SECRET_KEY not configured | Missing env var | Add to PythonAnywhere web app settings |
| NoReverseMatch client_email_login | Secondary error | Fix CLERK_SECRET_KEY first |
| OSError Network is unreachable | SMTP blocked | Use SendGrid instead |
| OTP not sent | API key invalid | Verify key format and value |
| Emails not arriving | SMTP/SendGrid down | Check service status |

---

## Support Resources

- **PythonAnywhere Help:** https://www.pythonanywhere.com/help/
- **Clerk API Docs:** https://clerk.com/docs
- **SendGrid Docs:** https://sendgrid.com/docs
- **Django Email:** https://docs.djangoproject.com/en/5.2/topics/email/

