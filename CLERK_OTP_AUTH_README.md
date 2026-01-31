# Clerk OTP Authentication Implementation Guide

## Overview

This document describes the new OTP-based email authentication system for clients in the Agnivridhi CRM. Clients can now log in using their email address and a one-time password (OTP) instead of traditional username/password authentication.

## Features

✅ **Email-based OTP Login**
- Clients enter their email address
- Receive a 6-digit OTP via email
- Enter OTP to log in securely
- No passwords needed

✅ **Automatic Setup on Approval**
- When a client is approved, automatic email notification is sent
- Client email is marked as ready for OTP login
- Welcome email with login instructions included

✅ **Security Features**
- OTP expires after 10 minutes
- Maximum 3 verification attempts per session
- Secure session management
- OTP stored in cache, not database

✅ **User Experience**
- Simple, intuitive login flow
- Professional email templates
- Clear error messages
- Responsive design

## Architecture

### Components

1. **Clerk Auth Service** (`accounts/clerk_auth.py`)
   - Generates and manages OTPs
   - Stores OTPs in Django cache
   - Verifies OTP and creates sessions
   - Handles email operations

2. **Authentication Views** (`accounts/views_otp_auth.py`)
   - `ClientEmailLoginView`: Email entry
   - `ClientVerifyOTPView`: OTP verification
   - `ClientLogoutView`: Logout
   - API endpoints for AJAX requests

3. **Signal Handler** (`clients/clerk_signals.py`)
   - Triggers on client approval
   - Sends welcome email
   - Logs authentication events

4. **Email Templates**
   - `templates/emails/clerk_auth_welcome.html`: Welcome email for approved clients
   - `templates/accounts/client_email_login.html`: Email login form
   - `templates/accounts/client_verify_otp.html`: OTP verification form

### Database Changes

**No new database models created.** The system uses:
- Existing `Client.contact_email` field
- Existing `Client.is_approved` field
- Django cache (configurable backend)

### Flow Diagram

```
CLIENT CREATED
    ↓
Client email captured (contact_email field)
    ↓
CLIENT APPROVED
    ↓
Signal triggers: clerk_signals.setup_clerk_auth_on_approval()
    ↓
Welcome email sent to client.contact_email
    ↓
CLIENT VISITS LOGIN PAGE (/accounts/client-login/)
    ↓
Enters email address
    ↓
OTP sent and cached
    ↓
Receives OTP in email
    ↓
Enters OTP at /accounts/client-verify-otp/
    ↓
OTP verified
    ↓
Django session created (login)
    ↓
Redirected to dashboard
```

## URL Routes

| Route | Purpose |
|-------|---------|
| `/accounts/client-login/` | Email entry page |
| `/accounts/client-verify-otp/` | OTP verification page |
| `/accounts/client-logout/` | Logout |
| `/accounts/api/send-otp/` | API: Send OTP |
| `/accounts/api/verify-otp/` | API: Verify OTP |

## Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# Clerk Configuration
CLERK_API_KEY=your_clerk_api_key_here
SITE_URL=https://yourdomain.com
COMPANY_NAME=Your Company Name

# Cache Configuration (for OTP storage)
CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache
CACHE_LOCATION=agnivridhi-cache
CACHE_TIMEOUT=300  # 5 minutes (OTP expires after 10 minutes by default)

# Email Configuration (for sending OTP and welcome emails)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=your-email-host.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=noreply@example.com
```

### Django Settings

Settings are automatically configured in `agnivridhi_crm/settings.py`:

```python
# Caching (for OTP)
CACHES = {
    'default': {
        'BACKEND': os.getenv('CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache'),
        'LOCATION': os.getenv('CACHE_LOCATION', 'agnivridhi-cache'),
        'OPTIONS': {
            'MAX_ENTRIES': 10000,
        },
        'TIMEOUT': 300,  # 5 minutes
    }
}

# Clerk Settings
CLERK_API_KEY = os.getenv('CLERK_API_KEY', '')
SITE_URL = os.getenv('SITE_URL', 'http://localhost:8000')
COMPANY_NAME = os.getenv('COMPANY_NAME', 'Agnivridhi India')
```

## Usage Examples

### 1. Client Login Flow (HTML Form)

```html
<!-- Step 1: Email Entry -->
<form method="POST" action="{% url 'client_email_login' %}">
    {% csrf_token %}
    <input type="email" name="email" placeholder="Enter your email" required>
    <button type="submit">Send OTP</button>
</form>

<!-- Step 2: OTP Verification -->
<form method="POST" action="{% url 'client_verify_otp' %}">
    {% csrf_token %}
    <input type="text" name="otp" placeholder="000000" maxlength="6" required>
    <button type="submit">Verify Code</button>
</form>
```

### 2. API Usage (JavaScript/AJAX)

```javascript
// Send OTP
fetch('/accounts/api/send-otp/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({email: 'client@example.com'})
})
.then(r => r.json())
.then(data => console.log(data.message))

// Verify OTP
fetch('/accounts/api/verify-otp/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({email: 'client@example.com', otp: '123456'})
})
.then(r => r.json())
.then(data => {
    if(data.success) {
        // Redirect to dashboard
        window.location.href = '/accounts/dashboard/client/';
    }
})
```

### 3. Manual Client Approval

```python
from clients.models import Client

# Admin approves client
client = Client.objects.get(id=1)
client.is_approved = True
client.approved_by = request.user
client.approved_at = timezone.now()
client.save()
# Signal automatically sends welcome email!
```

## Testing

### Test Scenarios

1. **Normal Flow**
   - Create client with email
   - Approve client
   - Verify welcome email sent
   - Login with email
   - Receive OTP
   - Enter OTP
   - Verify login successful

2. **Error Cases**
   - Invalid email (not in system)
   - Unapproved client attempts login (should be rejected)
   - Wrong OTP entered
   - OTP expired
   - Too many failed attempts

### Test Code

```python
from django.test import TestCase, Client as TestClient
from django.contrib.auth.models import User
from clients.models import Client

class ClerkAuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'pass123')
        self.client_obj = Client.objects.create(
            user=self.user,
            name='Test Company',
            contact_email='client@example.com',
            is_approved=True
        )
        self.client = TestClient()
    
    def test_email_login_page(self):
        response = self.client.get('/accounts/client-login/')
        self.assertEqual(response.status_code, 200)
    
    def test_send_otp(self):
        response = self.client.post('/accounts/client-login/', {
            'email': 'client@example.com'
        })
        # Should redirect to OTP verification
        self.assertEqual(response.status_code, 302)
```

## Deployment Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   # Update .env with email and cache settings
   nano .env
   ```

3. **Enable Caching** (if using Redis)
   ```bash
   # Install Redis
   pip install redis django[cache]
   
   # Update .env
   CACHE_BACKEND=django.core.cache.backends.redis.RedisCache
   REDIS_URL=redis://localhost:6379/0
   ```

4. **Test Locally**
   ```bash
   python manage.py runserver
   # Visit http://localhost:8000/accounts/client-login/
   ```

5. **Deploy to Production**
   ```bash
   git add .
   git commit -m "Add Clerk OTP authentication for clients"
   git push origin main
   
   # On server:
   python manage.py collectstatic --noinput
   python manage.py migrate
   systemctl restart agnivridhi_crm
   ```

## Security Considerations

✅ **OTP Security**
- Generated using `secrets.choice()` (cryptographically secure)
- Stored in cache with 10-minute expiration
- Never stored in database
- Deleted after successful verification

✅ **Session Security**
- Uses Django's session framework
- CSRF protection enabled
- SessionIdleTimeoutMiddleware enforces idle timeout
- SESSION_COOKIE_HTTPONLY=True (no JS access)

✅ **Email Security**
- Email not exposed in OTP message header
- One-time use code
- Limited verification attempts

## Troubleshooting

### OTP not received
- Check email configuration in settings
- Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
- Check spam folder
- Ensure client.contact_email is populated

### Client marked as unapproved
- Contact admin to approve via Django admin
- Check Client.is_approved field
- Welcome email only sent on approval

### Cache issues
- For development: Uses Django's in-memory cache (LocMemCache)
- For production: Configure Redis in .env
- Clear cache if OTP issues persist: `python manage.py shell`

## Future Enhancements

- [ ] Add Clerk SDK integration (OAuth tokens)
- [ ] Implement two-factor authentication (2FA)
- [ ] Add biometric login support
- [ ] Implement social login (Google, Microsoft)
- [ ] Add login activity logs
- [ ] Implement passwordless device registration
- [ ] Add multi-device session management

## Support

For issues or questions regarding Clerk OTP authentication:

1. Check logs: `tail -f /var/log/agnivridhi_crm.log`
2. Review email configuration
3. Verify Client model has contact_email populated
4. Check Django cache configuration
5. Contact support at support@agnivridhi.com

---

**Last Updated:** 2024
**Author:** Agnivridhi Development Team
**Status:** ✅ Production Ready
