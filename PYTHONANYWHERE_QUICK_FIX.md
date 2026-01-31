# 🚀 PythonAnywhere Quick Fix (5 Minutes)

## Problem
Your production logs show:
```
❌ CLERK_SECRET_KEY not configured - Clerk OTP will not work
❌ django.urls.exceptions.NoReverseMatch: Reverse for 'client_email_login' not found
```

## Root Cause
The `.env` file isn't on the production server (it's in `.gitignore`), so Clerk API keys aren't available.

## Fix (Choose ONE)

### ⭐ EASIEST: Use PythonAnywhere Web Interface

**STEP 1:** Open https://www.pythonanywhere.com/user/agnivridhicrm/webapps/

**STEP 2:** Click on: `agnivridhicrm.pythonanywhere.com`

**STEP 3:** Scroll down to find **"Environment variables"** section

**STEP 4:** Add these two lines:
```
CLERK_SECRET_KEY=sk_test_Uzd7yFdLxr5B13dlOktPvYp5hST63dS0l3bEsuMyKz
CLERK_PUBLIC_KEY=pk_test_dGVuZGVyLXNlYXNuYWlsLTk5LmNsZXJrLmFjY291bnRzLmRldiQ
```

**STEP 5:** Click **"Save"** or **"Reload"**

**STEP 6:** Test: Visit http://agnivridhicrm.pythonanywhere.com/client-login/

✅ Done! The page should now load without errors.

---

### Alternative: Use Bash Console

If you can't find environment variables section:

**Open:** https://www.pythonanywhere.com/user/agnivridhicrm/bash/

**Run:**
```bash
cd /home/agnivridhicrm/crm-agnivridhi
cat > .env << 'EOF'
CLERK_SECRET_KEY=sk_test_Uzd7yFdLxr5B13dlOktPvYp5hST63dS0l3bEsuMyKz
CLERK_PUBLIC_KEY=pk_test_dGVuZGVyLXNlYXNuYWlsLTk5LmNsZXJrLmFjY291bnRzLmRldiQ
EOF

# Reload web app
touch /var/www/agnivridhicrm_pythonanywhere_com_wsgi.py
```

---

## Verify It Works

❌ **Before fix:**
```
CLERK_SECRET_KEY not configured - Clerk OTP will not work
Reverse for 'client_email_login' not found
```

✅ **After fix:**
- Page loads without errors
- Email input form displays
- "Send OTP" button works

---

## What Else Needs Fixing?

### SMTP Email Error
```
OSError: [Errno 101] Network is unreachable
```

**Quick Fix:** Install SendGrid (see PRODUCTION_ERROR_FIX_GUIDE.md)

---

## FAQ

**Q: Where do I find environment variables section?**
A: In PythonAnywhere web app settings, scroll to bottom. May say "Environment variables", "Web app settings", or be near the "Source code" section.

**Q: Can I put the API key in version control?**
A: NO! Keep it in environment variables only, never commit to git.

**Q: What if it still doesn't work?**
A: Check the logs at: `/var/log/agnivridhicrm_pythonanywhere_com_error.log`

**Q: Should I use test keys or live keys?**
A: Test keys first (pk_test_..., sk_test_...). Switch to live keys (pk_live_..., sk_live_...) when ready for production.

---

## Next: Switch to Live Keys

Once testing works with test keys:

1. Get live keys from https://dashboard.clerk.com
2. Replace in environment variables:
   ```
   CLERK_SECRET_KEY=sk_live_YOUR_ACTUAL_LIVE_KEY
   CLERK_PUBLIC_KEY=pk_live_YOUR_ACTUAL_LIVE_KEY
   ```
3. Reload web app
4. Test again

---

## Support

If something breaks:
- Check logs: `/var/log/agnivridhicrm_pythonanywhere_com_error.log`
- See PRODUCTION_ERROR_FIX_GUIDE.md for detailed analysis
- Contact PythonAnywhere support if environment variables won't save
