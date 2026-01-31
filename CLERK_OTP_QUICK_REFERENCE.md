# Clerk OTP Authentication - Quick Reference Card

## 🚀 TL;DR - Setup in 3 Steps

### Step 1: Get Clerk API Keys
```
1. Go to https://dashboard.clerk.com
2. Sign up (free)
3. Go to Settings → API Keys
4. Copy pk_live_xxx and sk_live_xxx
```

### Step 2: Add to `.env`
```
CLERK_PUBLIC_KEY=pk_live_xxxxxxxxxxxx
CLERK_SECRET_KEY=sk_live_xxxxxxxxxxxx
```

### Step 3: Test Locally
```bash
python manage.py runserver
# Visit: http://localhost:8000/accounts/client-login/
# Enter email → Get OTP → Enter OTP
```

---

## 📋 Files Changed

```
✏️  accounts/clerk_otp_service.py     (NEW - REST API service)
✏️  accounts/views_otp_auth.py        (Updated import)
✏️  agnivridhi_crm/settings.py        (Added Clerk config)
✏️  .env                               (Added Clerk keys)
✏️  .env.pythonanywhere                (Added Clerk keys)
```

---

## 🔑 API Endpoints

### Send OTP
```
POST https://api.clerk.com/v1/sign_ins
{
    "strategy": "email_code",
    "identifier": "user@email.com"
}
Returns: { "id": "signin_xxx", ... }
```

### Verify OTP  
```
PATCH https://api.clerk.com/v1/sign_ins/{signin_id}/attempt_verification
{
    "code": "123456",
    "strategy": "email_code"
}
Returns: { "status": "complete", "created_user_id": "user_xxx", ... }
```

---

## 🧪 Test Commands

### Local Testing
```bash
# Start Django
python manage.py runserver

# Visit
http://localhost:8000/accounts/client-login/

# OR test via Python shell
python manage.py shell
>>> from accounts.clerk_otp_service import clerk_service
>>> result = clerk_service.send_otp('test@example.com')
>>> print(result)
```

### PythonAnywhere Deployment
```bash
# SSH into server
cd ~/agnivridhi.pythonanywhere.com
git pull origin main

# Then reload web app in PythonAnywhere dashboard
```

---

## ⚙️ Configuration Checklist

- [ ] Clerk account created (https://dashboard.clerk.com)
- [ ] API keys obtained (pk_live_* and sk_live_*)
- [ ] `.env` updated with CLERK_PUBLIC_KEY and CLERK_SECRET_KEY
- [ ] Tested locally (OTP sent and verified)
- [ ] Pushed to GitHub
- [ ] PythonAnywhere environment variables set
- [ ] Git pulled on PythonAnywhere server
- [ ] Web app reloaded on PythonAnywhere
- [ ] Tested on production (https://agnivridhicrm.pythonanywhere.com/accounts/client-login/)

---

## 🔍 Error Codes

| Error | Cause | Fix |
|-------|-------|-----|
| "OTP service not configured" | Missing CLERK_SECRET_KEY | Add to `.env` or PythonAnywhere env vars |
| "Failed to send OTP" | Invalid API key or network issue | Verify keys in Clerk dashboard |
| "Invalid OTP code" | Expired or wrong code | User should request new OTP |
| "HTTP 401 Unauthorized" | Bad CLERK_SECRET_KEY | Check Clerk dashboard for correct key |

---

## 📊 Architecture

```
User                Client Login View           Clerk API
  │                      │                          │
  ├──Enter Email──>     │                          │
  │                      ├──POST /sign_ins────────>│
  │                      │<─────signin_id──────────┤
  │                      │                          │
  │<──Show OTP Input──   │                          │
  │                      │  (Email sent to user)    │
  │──Enter OTP────>     │                          │
  │                      ├──PATCH /attempt_verify──>│
  │                      │<─────{status: complete}──┤
  │                      │                          │
  │<──Login Success──   │                          │
```

---

## 🛡️ Security

- ✅ All API calls use HTTPS
- ✅ OTP codes never stored in database
- ✅ Rate limiting by Clerk (prevent brute force)
- ✅ API keys in environment variables (not git)
- ✅ Session tokens created by Clerk

---

## 📞 Support Resources

- **Clerk Docs:** https://clerk.com/docs/authentication/email-otp
- **API Reference:** https://clerk.com/docs/reference/backend-api
- **Status Page:** https://clerk.statuspage.io

---

## 💡 Tips

1. **Test Keys:** Use pk_test_* for testing in dev
2. **Email Templates:** Customize in Clerk Dashboard → Email Templates
3. **OTP Duration:** Default is 10 min (configurable)
4. **Multi-tenant:** Set organization_id if needed
5. **Rate Limits:** ~10 OTPs per user per hour

---

## ✅ Verification Checklist

After setup, verify these work:

```bash
✓ python manage.py check
✓ python manage.py runserver (no import errors)
✓ GET  /accounts/client-login/  (shows form)
✓ POST /accounts/client-login/  (with email - OTP sent)
✓ OTP email received
✓ POST /accounts/verify-otp/    (with OTP code - verified)
✓ Redirected to dashboard (logged in)
```

---

## 📝 Notes

- **No SDK needed:** Uses REST API + requests library
- **Works everywhere:** PythonAnywhere free tier supported
- **Automatic emails:** Clerk handles all email delivery
- **Django integration:** Syncs with Django User model
- **Logging:** All events logged to Django logger

---

**Last Updated:** 2024
**Status:** Production Ready ✅
