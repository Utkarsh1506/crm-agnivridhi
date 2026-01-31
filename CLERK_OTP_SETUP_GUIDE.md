# Clerk OTP Authentication - Setup & Deployment Guide

## Overview

This guide explains how to set up and deploy Clerk-based OTP authentication for your Agnivridhi CRM application. This system replaces the previous manual SMTP email approach with Clerk's professional authentication service.

**Benefits:**
- ✅ Works on PythonAnywhere free tier (no SMTP restrictions)
- ✅ Professional OTP delivery by Clerk
- ✅ Automatic email handling
- ✅ More reliable than manual SMTP
- ✅ No additional Python dependencies required

---

## Step 1: Create Clerk Account

### 1.1 Sign Up
1. Visit: https://dashboard.clerk.com
2. Sign up with your email (free tier available)
3. Confirm your email
4. Log in to the dashboard

### 1.2 Get Your API Keys
1. In Clerk Dashboard, go to **Settings** → **API Keys**
2. Copy your keys:
   - **`CLERK_PUBLIC_KEY`** - Starts with `pk_live_` or `pk_test_`
   - **`CLERK_SECRET_KEY`** - Starts with `sk_live_` or `sk_test_`
3. Save these keys securely (don't commit to git)

### 1.3 Enable Email Code Strategy
1. Go to **User & Authentication** → **Authentication Methods**
2. Ensure **Email Code** is enabled (should be default)
3. Configure email settings if needed

---

## Step 2: Configure Local Development

### 2.1 Update `.env` File

Edit `.env` in your project root:

```dotenv
# Clerk Authentication Configuration
CLERK_PUBLIC_KEY=pk_live_xxxxxxxxxxxxxxxxxxxx
CLERK_SECRET_KEY=sk_live_xxxxxxxxxxxxxxxxxxxx
```

Replace `xxxxxxxxxxxxxxxxxxxx` with your actual keys from Clerk dashboard.

### 2.2 Verify Configuration

Test your setup:

```bash
python manage.py shell
```

Then in the Python shell:

```python
from accounts.clerk_otp_service import clerk_service
print(clerk_service.clerk_api_key)  # Should show your secret key
```

### 2.3 Test OTP Flow Locally

```bash
python manage.py runserver
```

Visit: http://localhost:8000/accounts/client-login/

1. Enter a test email address
2. You should receive an OTP email from Clerk
3. Enter the OTP to verify

---

## Step 3: Deploy to PythonAnywhere

### 3.1 Push to GitHub

```bash
git add -A
git commit -m "Clerk OTP setup"
git push origin main
```

### 3.2 Update PythonAnywhere Environment

1. Log in to PythonAnywhere
2. Open **Web** tab and click your app
3. Go to **WSGI configuration file** 
4. Ensure settings use `.env.pythonanywhere`

OR

3. Go to **Settings** → **Environment Variables**
4. Add:
   ```
   CLERK_PUBLIC_KEY=pk_live_xxxxxxxxxxxxxxxxxxxx
   CLERK_SECRET_KEY=sk_live_xxxxxxxxxxxxxxxxxxxx
   ```

### 3.3 Update Code on PythonAnywhere

SSH into PythonAnywhere:

```bash
cd ~/agnivridhi.pythonanywhere.com
git pull origin main
```

### 3.4 Reload Web App

In PythonAnywhere dashboard:
- Click **Web** tab
- Click **Reload** button

### 3.5 Test Deployment

Visit: https://agnivridhicrm.pythonanywhere.com/accounts/client-login/

Test the same flow:
1. Enter test email
2. Check inbox for OTP
3. Enter OTP

---

## Code Architecture

### Files Updated

#### 1. `accounts/clerk_otp_service.py` (NEW)
Implements Clerk OTP service using REST API:
- `send_otp(email)` - Initiates OTP flow
- `verify_otp(sign_in_id, otp_code)` - Verifies OTP code
- `get_or_create_user()` - Syncs Clerk user with Django user

#### 2. `accounts/views_otp_auth.py` (MODIFIED)
Updated imports:
```python
# Changed from:
from accounts.clerk_auth import clerk_service
# To:
from accounts.clerk_otp_service import clerk_service
```

#### 3. `agnivridhi_crm/settings.py` (MODIFIED)
Added Clerk configuration:
```python
CLERK_PUBLIC_KEY = os.getenv('CLERK_PUBLIC_KEY', '')
CLERK_SECRET_KEY = os.getenv('CLERK_SECRET_KEY', '')
```

#### 4. `.env` (MODIFIED)
Added Clerk keys for local development

#### 5. `.env.pythonanywhere` (MODIFIED)
Added Clerk keys for production

#### 6. `requirements.txt` (NO CHANGE NEEDED)
Uses existing `requests` library for API calls

---

## API Details

### Clerk REST API Endpoints Used

#### Send OTP
```
POST https://api.clerk.com/v1/sign_ins
Authorization: Bearer sk_live_xxxxx
Content-Type: application/json

{
    "strategy": "email_code",
    "identifier": "user@example.com"
}

Response:
{
    "id": "signin_xxx",
    "status": "needs_first_factor",
    ...
}
```

#### Verify OTP
```
PATCH https://api.clerk.com/v1/sign_ins/{signin_id}/attempt_verification
Authorization: Bearer sk_live_xxxxx
Content-Type: application/json

{
    "code": "123456",
    "strategy": "email_code"
}

Response:
{
    "id": "signin_xxx",
    "status": "complete",
    "created_user_id": "user_xxx",
    "created_session_id": "sess_xxx"
}
```

---

## Troubleshooting

### Issue: "OTP service not configured"

**Cause:** CLERK_SECRET_KEY environment variable not set

**Solution:**
1. Verify `.env` has Clerk keys
2. Restart Django: `python manage.py runserver`
3. On PythonAnywhere: Reload web app

### Issue: "Failed to send OTP"

**Cause:** Invalid Clerk API key or network issue

**Solution:**
1. Verify API keys in Clerk dashboard
2. Check internet connection
3. Verify Clerk account has email code strategy enabled

### Issue: OTP Email Not Received

**Cause:** Email domain issues or spam filtering

**Solution:**
1. Check spam/promotions folder
2. Verify email address is correct
3. Contact Clerk support if domain blocklisted

### Issue: "Invalid OTP code"

**Cause:** Code expired or mistyped

**Solution:**
- OTP codes expire after 10 minutes
- User should request new OTP if expired
- Ensure code is copied correctly (no spaces)

---

## Monitoring & Logging

Check logs for debugging:

### Local Development
```bash
# In Django settings, logging is configured for 'accounts' logger
tail -f logs/debug.log | grep CLERK
```

### PythonAnywhere
1. Go to **Web** tab
2. Click **Error log** to see issues
3. Search for "CLERK" entries

### Expected Log Messages
```
ClerkOTPService initialized
Sending OTP to user@example.com via Clerk API
OTP sent successfully to user@example.com, sign_in_id: signin_xxx
Verifying OTP for sign-in: signin_xxx
OTP verified successfully, user_id: user_xxx
```

---

## Security Notes

1. **Never commit `.env`** - Add to `.gitignore` (already done)
2. **Protect API Keys:**
   - Keep CLERK_SECRET_KEY confidential
   - Use environment variables, not hardcoded values
   - Rotate keys periodically in Clerk dashboard
3. **Rate Limiting:**
   - Clerk implements rate limiting on OTP requests
   - Users can't request more than X OTPs per hour
4. **SSL/TLS:**
   - All Clerk API calls use HTTPS
   - Ensure PythonAnywhere has SSL enabled (it does by default)

---

## FAQ

### Q: Can I test with a test API key?
**A:** Yes! Create a test project in Clerk and use test keys (pk_test_* and sk_test_*). Results won't be live.

### Q: What happens when user clicks "Send OTP" multiple times?
**A:** Each request creates a new sign-in session. Only the latest OTP code is valid.

### Q: Can I customize the OTP email template?
**A:** Yes, in Clerk Dashboard → Email Templates. Customize for your branding.

### Q: How long is OTP valid?
**A:** By default, 10 minutes (configurable in Clerk settings).

### Q: Do I need to store OTP codes in the database?
**A:** No! Clerk handles everything. Your code just passes sign_in_id and OTP code.

### Q: Will this work on custom domains?
**A:** Yes! As long as CLERK_SECRET_KEY is set in environment variables.

---

## Next Steps

1. ✅ Create Clerk account
2. ✅ Get API keys
3. ✅ Update `.env` with Clerk keys
4. ✅ Test locally
5. ✅ Push to GitHub
6. ✅ Deploy to PythonAnywhere
7. ✅ Update PythonAnywhere environment variables
8. ✅ Test in production

---

## Support

- **Clerk Documentation:** https://clerk.com/docs
- **Your Email:** Add support contact if needed
- **Logs:** Check Django logs for detailed error messages

---

## Changelog

- **2024** - Migrated from manual SMTP to Clerk REST API
  - No SDK dependencies required
  - Works on PythonAnywhere free tier
  - Uses existing requests library
  - Automatic email handling by Clerk
