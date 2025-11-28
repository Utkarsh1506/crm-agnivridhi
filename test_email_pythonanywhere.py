#!/usr/bin/env python
"""
Quick SMTP Test Script for PythonAnywhere
Copy and paste this entire script in PythonAnywhere Bash console
"""

import os
import sys

# Add your project to Python path
sys.path.insert(0, '/home/agnivridhicrm/crm-agnivridhi')

# Set Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'agnivridhi_crm.settings'

# Setup Django
import django
django.setup()

# Now test email
from django.core.mail import send_mail
from django.conf import settings

print("="*60)
print("SMTP CONFIGURATION TEST - PythonAnywhere")
print("="*60)

print(f"\n✓ EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"✓ EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"✓ EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"✓ EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"✓ EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"✓ DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

print("\n" + "="*60)
print("SENDING TEST EMAIL...")
print("="*60)

try:
    send_mail(
        subject='✅ SendGrid Test from PythonAnywhere',
        message='If you receive this, SendGrid is working perfectly on PythonAnywhere!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['vharadharajharshitha@gmail.com'],
        fail_silently=False,
    )
    print("\n🎉 SUCCESS! Email sent successfully!")
    print("Check the inbox (and spam folder) for the test email.")
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"Message: {str(e)}")
    print("\nPossible causes:")
    print("1. WSGI file not updated with SendGrid settings")
    print("2. Web app not reloaded after WSGI changes")
    print("3. SendGrid API key invalid or expired")
    print("4. EMAIL_HOST is not 'smtp.sendgrid.net'")
