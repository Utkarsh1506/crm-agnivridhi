# Gmail App Password Setup Guide for Agnivridhi CRM

## Step 1: Enable 2-Step Verification

1. Go to: https://myaccount.google.com/security
2. Find "2-Step Verification" section
3. Click "2-Step Verification"
4. Follow steps to enable it (if not already enabled)

## Step 2: Create App Password

1. Go to: https://myaccount.google.com/apppasswords
   (Or: Google Account → Security → 2-Step Verification → App passwords)

2. You might need to sign in again

3. In "Select app" dropdown:
   - Choose "Mail"

4. In "Select device" dropdown:
   - Choose "Other (Custom name)"
   - Type: "Agnivridhi CRM"

5. Click "Generate"

6. Google will show a 16-character password like: `abcd efgh ijkl mnop`

7. **COPY THIS PASSWORD** (you won't see it again!)

## Step 3: Update WSGI File on PythonAnywhere

1. Go to PythonAnywhere Dashboard → Web tab

2. Click on your WSGI configuration file link:
   `/var/www/agnivridhicrm_pythonanywhere_com_wsgi.py`

3. Replace the entire content with this:

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

# Email Configuration - Gmail SMTP
os.environ['EMAIL_BACKEND'] = 'django.core.mail.backends.smtp.EmailBackend'
os.environ['EMAIL_HOST'] = 'smtp.gmail.com'
os.environ['EMAIL_PORT'] = '587'
os.environ['EMAIL_USE_TLS'] = 'True'
os.environ['EMAIL_HOST_USER'] = 'utkarshchoudhary1573@gmail.com'
os.environ['EMAIL_HOST_PASSWORD'] = 'PASTE_YOUR_APP_PASSWORD_HERE'  # ← Paste the 16-char password here
os.environ['DEFAULT_FROM_EMAIL'] = 'Agnivridhi CRM <utkarshchoudhary1573@gmail.com>'

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

4. In line with `EMAIL_HOST_PASSWORD`, **paste the 16-character password** (remove spaces)

5. Click "Save" (green button at top)

## Step 4: Reload Web App

1. Go back to Web tab
2. Click the big green "Reload" button
3. Wait for reload to complete

## Step 5: Test Email

Go to PythonAnywhere → Consoles → Bash

```bash
cd ~/crm-agnivridhi
python manage.py shell
```

In the Python shell:
```python
from django.core.mail import send_mail
from django.conf import settings

print("Testing Gmail SMTP...")
print(f"Host: {settings.EMAIL_HOST}")
print(f"User: {settings.EMAIL_HOST_USER}")

send_mail(
    'Test from Agnivridhi CRM',
    'Gmail SMTP is working!',
    settings.DEFAULT_FROM_EMAIL,
    ['vharadharajharshitha@gmail.com'],
    fail_silently=False,
)
print("✅ Email sent successfully!")
```

## Troubleshooting

### Error: "Username and Password not accepted"
- Make sure you used the **App Password**, not your regular Gmail password
- Check that 2-Step Verification is enabled
- Regenerate a new App Password if needed

### Error: "Connection timed out"
- Gmail SMTP is whitelisted on PythonAnywhere, this shouldn't happen
- Check that EMAIL_PORT is '587' (string, not integer)

### Error: "SMTPAuthenticationError"
- Double-check the App Password (no spaces)
- Make sure EMAIL_HOST_USER is your full Gmail address

### Emails going to Spam
- This is normal for new Gmail senders
- Ask recipients to mark as "Not Spam"
- Consider adding SPF/DKIM records for your domain later

## Security Notes

- ✅ App Passwords are safer than regular passwords
- ✅ You can revoke App Password anytime from Google Account
- ✅ Don't commit the App Password to Git (it's in WSGI file, not code)
- ✅ Each app should have its own App Password

## Alternative: Use Your Custom Domain with Gmail

If you want to send from noreply@agnivridhiindia.com but use Gmail SMTP:

1. Set up Gmail with your custom domain (requires Google Workspace)
2. Or use SendGrid/Mailgun with verified domain (recommended for production)

For now, using utkarshchoudhary1573@gmail.com is fine for testing and initial deployment.
