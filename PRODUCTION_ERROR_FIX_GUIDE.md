# Production Error Analysis & Fix Guide

## Error Summary

Your PythonAnywhere logs show 3 distinct errors:

### Error 1: CLERK_SECRET_KEY Not Configured ❌
```
CLERK_SECRET_KEY not configured - Clerk OTP will not work
CLERK_SECRET_KEY not configured - checked at send_otp time
```
**Root Cause:** `.env` file missing on PythonAnywhere server  
**Impact:** OTP authentication completely broken  
**Fix:** Set environment variables in PythonAnywhere

### Error 2: URL Reverse Error ❌
```
django.urls.exceptions.NoReverseMatch: Reverse for 'client_email_login' not found
```
**Root Cause:** Secondary error - OTP service fails to load, template rendering fails  
**Impact:** `/client-login/` page doesn't load  
**Fix:** Resolves automatically when Error 1 is fixed

### Error 3: SMTP Network Error ❌
```
OSError: [Errno 101] Network is unreachable
```
**Root Cause:** Django trying to send emails via SMTP; PythonAnywhere free tier blocks SMTP  
**Impact:** Password reset/forgot password emails won't send  
**Fix:** Use SendGrid or Clerk's built-in email instead

---

## Fix #1: CLERK_SECRET_KEY Configuration (CRITICAL)

### Option A: PythonAnywhere Web Interface (SIMPLEST) ⭐

1. Go to: https://www.pythonanywhere.com/user/agnivridhicrm/webapps/
2. Click on `agnivridhicrm.pythonanywhere.com`
3. Scroll down to find **"Web app settings"** or **"Source code"** section
4. Look for **Environment variables** section (or **Web app configuration**)
5. Add these variables:

```
CLERK_SECRET_KEY=sk_test_Uzd7yFdLxr5B13dlOktPvYp5hST63dS0l3bEsuMyKz
CLERK_PUBLIC_KEY=pk_test_dGVuZGVyLXNlYXNuYWlsLTk5LmNsZXJrLmFjY291bnRzLmRldiQ
```

6. **Click Reload** to apply changes
7. Test: Visit http://agnivridhicrm.pythonanywhere.com/client-login/

### Option B: Bash Console (Create .env File)

1. Go to: https://www.pythonanywhere.com/user/agnivridhicrm/files/
2. Click **"Open bash console here"**
3. Run:

```bash
cd /home/agnivridhicrm/crm-agnivridhi

# Create .env file with your configuration
cat > .env << 'EOF'
DEBUG=False
SECRET_KEY=django-insecure-w=1cy8to$#w_@okqkg)^x3c%q=4^5xnnju2br(lmuhe&)q)kq_
ALLOWED_HOSTS=agnivridhicrm.pythonanywhere.com
CLERK_SECRET_KEY=sk_test_Uzd7yFdLxr5B13dlOktPvYp5hST63dS0l3bEsuMyKz
CLERK_PUBLIC_KEY=pk_test_dGVuZGVyLXNlYXNuYWlsLTk5LmNsZXJrLmFjY291bnRzLmRldiQ
EOF

# Verify
cat .env

# Set secure permissions
chmod 600 .env

# Restart web app
touch /var/www/agnivridhicrm_pythonanywhere_com_wsgi.py
```

4. Test: Refresh http://agnivridhicrm.pythonanywhere.com/client-login/

---

## Fix #2: SMTP Email Configuration

### Quick Fix: Use Console Email Backend (Development Only)
For testing without email sending:

```python
# In settings.py or via environment variable:
EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
```

Emails will print to console instead of failing.

### Production Fix: Use SendGrid

1. **Get SendGrid API Key:**
   - Sign up: https://sendgrid.com
   - Create API key with "Mail Send" permission

2. **Install SendGrid Package:**
   ```bash
   pip install django-sendgrid-v5
   ```

3. **Update requirements.txt:**
   ```
   django-sendgrid-v5==1.10.2
   ```

4. **Update settings.py:**
   ```python
   EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
   SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')
   DEFAULT_FROM_EMAIL = 'noreply@agnivridhi.com'
   ```

5. **Set environment variable on PythonAnywhere:**
   ```
   SENDGRID_API_KEY=SG.your_sendgrid_api_key_here
   ```

### Alternative: Use Clerk's Email (Recommended)
Clerk handles sending OTP emails internally - no configuration needed!

---

## Verification Steps

### 1. Check Environment Variables Are Set
```bash
cd /home/agnivridhicrm/crm-agnivridhi
python -c "
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path('.env'))
print('CLERK_SECRET_KEY set:', bool(os.getenv('CLERK_SECRET_KEY')))
print('CLERK_PUBLIC_KEY set:', bool(os.getenv('CLERK_PUBLIC_KEY')))
print('Key length:', len(os.getenv('CLERK_SECRET_KEY', '')))
"
```

### 2. Test OTP Endpoint
```bash
# Test via Django shell
python manage.py shell
```

```python
from accounts.clerk_otp_service import clerk_service

# Test send OTP
result = clerk_service.send_otp('test@example.com')
print(result)
```

### 3. Check Django Logs
```bash
tail -f /var/log/agnivridhicrm_pythonanywhere_com_error.log
```

Look for:
- ✅ `ClerkOTPService initialized - Key present: True` (Good!)
- ✅ `Successfully created sign-in` (Good!)
- ❌ `CLERK_SECRET_KEY not configured` (Bad - fix needed)

### 4. Test in Browser
Visit: http://agnivridhicrm.pythonanywhere.com/client-login/

Should see:
- ✅ Email entry form loads
- ✅ No error messages about "not configured"
- ✅ No template reverse errors

---

## Checklist: Complete Production Setup

### Clerk OTP Authentication
- [ ] CLERK_SECRET_KEY environment variable set
- [ ] CLERK_PUBLIC_KEY environment variable set
- [ ] `/client-login/` page loads without errors
- [ ] OTP form accepts email input
- [ ] "Send OTP" button visible and functional

### Email Configuration
- [ ] Email backend configured (SendGrid or Console)
- [ ] Emails testing successful
- [ ] No SMTP network errors in logs

### General Django Settings
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS includes agnivridhicrm.pythonanywhere.com
- [ ] SECRET_KEY is set (unique, secure)
- [ ] CSRF_TRUSTED_ORIGINS configured

### Git & Database
- [ ] Latest code pulled from main branch
- [ ] Database migrations applied: `python manage.py migrate`
- [ ] Static files collected: `python manage.py collectstatic`

---

## Common Issues & Solutions

### Issue: "CLERK_SECRET_KEY not configured" persists
**Solution:**
1. Make sure you clicked **Reload** in PythonAnywhere web app settings
2. Wait 30 seconds for reload to complete
3. Check variable name spelling (case-sensitive!)
4. Try Option B (create .env file) instead

### Issue: "Network is unreachable" SMTP errors
**Solution:**
1. PythonAnywhere free tier blocks SMTP
2. Use SendGrid instead (see above)
3. Or use Console email backend for testing

### Issue: "NoReverseMatch" error persists
**Solution:**
1. This is secondary to CLERK configuration
2. Fix CLERK_SECRET_KEY first
3. Error should resolve automatically
4. If persists, check views_otp_auth.py is properly imported

### Issue: Database connection errors
**Solution:**
```bash
python manage.py migrate --database=default
python manage.py collectstatic --noinput
touch /var/www/agnivridhicrm_pythonanywhere_com_wsgi.py
```

---

## Testing in Local Development First

Before pushing to production, test locally:

```bash
# Create .env locally
echo "CLERK_SECRET_KEY=sk_test_..." > .env

# Test OTP sending
python manage.py shell

# In shell:
from accounts.clerk_otp_service import clerk_service
result = clerk_service.send_otp('your-test@email.com')
print(result)
```

If this fails locally, it will definitely fail in production!

---

## Production URLs After Fix

Once fixed, these URLs should work:

- ✅ `/client-login/` - Email entry form
- ✅ `/client-verify-otp/` - OTP verification form  
- ✅ `/api/send-otp/` - API endpoint for OTP
- ✅ `/api/verify-otp/` - API endpoint for verification

---

## Emergency: Rollback to Previous Version

If anything breaks:

```bash
cd /home/agnivridhicrm/crm-agnivridhi
git log --oneline -5
git revert HEAD  # Or git reset --hard <commit_hash>
touch /var/www/agnivridhicrm_pythonanywhere_com_wsgi.py
```

---

## Next Steps

1. **Immediate:** Set CLERK_SECRET_KEY environment variable (take 5 minutes)
2. **Test:** Verify `/client-login/` page loads
3. **Email:** Configure SendGrid (take 10 minutes)
4. **Deploy:** Push any code changes and reload
5. **Monitor:** Check logs for "successfully created sign-in" messages

**Expected Timeline:** 15-20 minutes total

