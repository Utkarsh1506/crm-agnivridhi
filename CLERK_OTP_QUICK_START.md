# Quick Start: Clerk OTP Authentication Setup

## What Was Added?

A complete OTP-based email authentication system for clients. Instead of usernames/passwords, clients now:
1. Enter their email
2. Receive a 6-digit OTP code
3. Enter the code to log in

**Automatic workflow:** When a client is approved → they automatically get a welcome email → they can log in with OTP

## File Structure

```
accounts/
  ├── clerk_auth.py                 # OTP generation & verification service
  ├── views_otp_auth.py             # Login views & API endpoints
  └── urls.py                        # Updated with new routes

clients/
  ├── clerk_signals.py              # Signal to send email on approval
  └── apps.py                        # Updated to register signals

templates/
  ├── accounts/
  │   ├── client_email_login.html    # Step 1: Email entry
  │   └── client_verify_otp.html     # Step 2: OTP entry
  └── emails/
      └── clerk_auth_welcome.html    # Welcome email template

agnivridhi_crm/
  └── settings.py                    # Cache & Clerk config added
```

## Setup Instructions

### 1. Configure Environment Variables

Add to your `.env` file:

```bash
# Email (required for sending OTP and welcome emails)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com          # or your email provider
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password  # Gmail: Generate app-specific password
DEFAULT_FROM_EMAIL=noreply@agnivridhi.com

# Optional: Clerk API (for future enhancements)
CLERK_API_KEY=your_clerk_key
SITE_URL=https://yourdomain.com
COMPANY_NAME=Agnivridhi India

# Cache (for storing OTPs temporarily)
CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache
CACHE_TIMEOUT=300  # 5 minutes (OTP expires after 10 mins by code)
```

### 2. Test Locally

```bash
# Start Django development server
python manage.py runserver

# Visit the login page
open http://localhost:8000/accounts/client-login/
```

**In development mode:** OTP will be printed to console and returned in API responses for testing.

### 3. Test the Flow

```python
# In Django shell
python manage.py shell

from clients.models import Client
from django.contrib.auth.models import User

# Create a client with email
user = User.objects.create_user('testclient', 'test@example.com', 'pass123')
client = Client.objects.create(
    user=user,
    name='Test Company',
    contact_email='test@example.com',  # THIS IS THE EMAIL THEY'LL USE TO LOGIN
    is_approved=False
)

# Simulate approval (this triggers the welcome email automatically)
client.is_approved = True
client.approved_by = User.objects.get(is_staff=True).first()  # Some staff user
client.save()  # 🎉 Welcome email sent automatically!
```

### 4. Deploy to Production

```bash
# 1. Commit and push changes
git add -A
git commit -m "Enable Clerk OTP authentication"
git push origin main

# 2. On your server, pull changes
git pull origin main

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Restart application
systemctl restart agnivridhi  # or your service name

# 5. (Optional) Configure Redis for better caching
pip install redis
# Update .env with CACHE_BACKEND=django.core.cache.backends.redis.RedisCache
```

## Usage

### For Admins/Staff:

**Creating a new client:**
1. Go to Django admin → Clients
2. Create client and fill in `contact_email` field
3. Check `is_approved` when ready
4. Save → Welcome email automatically sent! ✉️

### For Clients:

**Logging in:**
1. Go to `/accounts/client-login/`
2. Enter email
3. Check email for OTP code
4. Enter OTP code
5. ✅ Logged in!

### API Endpoints

**Send OTP:**
```bash
curl -X POST http://localhost:8000/accounts/api/send-otp/ \
  -H "Content-Type: application/json" \
  -d '{"email": "client@example.com"}'
```

**Verify OTP:**
```bash
curl -X POST http://localhost:8000/accounts/api/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{"email": "client@example.com", "otp": "123456"}'
```

## Key Points

✅ **No password needed** - Just email + OTP
✅ **Automatic setup** - Welcome email sent on approval
✅ **Secure** - OTP expires in 10 minutes, stored in cache only
✅ **Rate limited** - Max 3 failed attempts per session  
✅ **Professional UI** - Mobile-responsive, modern design
✅ **Email configurable** - Works with any SMTP provider

## Troubleshooting

**OTP not received?**
- Check Email configuration in `.env`
- Verify client.contact_email is populated
- Check spam/junk folder
- In development, OTP is logged to console

**Client can't log in?**
- Check `client.is_approved = True`
- Verify `contact_email` is set
- Clear browser cache
- Check browser console for errors

**Want to see OTP in development?**
- Check Django console output
- API responses include OTP in DEBUG mode
- Check email backend output

## File Descriptions

| File | Purpose |
|------|---------|
| `clerk_auth.py` | Service class for OTP generation/verification |
| `views_otp_auth.py` | View classes and API endpoints |
| `clerk_signals.py` | Auto-send welcome email on approval |
| `client_email_login.html` | Step 1 form template |
| `client_verify_otp.html` | Step 2 form template |
| `clerk_auth_welcome.html` | Welcome email template |
| `CLERK_OTP_AUTH_README.md` | Complete documentation |

## Next Steps

1. ✅ Review the templates - customize UI if needed
2. ✅ Configure email in `.env`
3. ✅ Test locally
4. ✅ Deploy to server
5. ✅ Create a test client and verify flow

## Questions?

Refer to `CLERK_OTP_AUTH_README.md` for comprehensive documentation covering:
- Architecture details
- Security considerations
- Testing examples
- Future enhancements

---

**Status:** ✅ Ready to use in production
**Last Updated:** 2024
