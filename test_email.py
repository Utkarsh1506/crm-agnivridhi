#!/usr/bin/env python
"""
Test SMTP email configuration for Agnivridhi CRM
Run this script to verify email settings are working correctly
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_smtp_configuration():
    """Test SMTP settings and send a test email"""
    print("="*60)
    print("SMTP CONFIGURATION TEST")
    print("="*60)
    
    # Display current settings
    print(f"\n✓ EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"✓ EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"✓ EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"✓ EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"✓ EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"✓ DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    # Check if using console backend
    if 'console' in settings.EMAIL_BACKEND.lower():
        print("\n⚠️  WARNING: You are using console backend!")
        print("   Emails will be printed to console, not sent via SMTP.")
        print("   Change EMAIL_BACKEND to 'django.core.mail.backends.smtp.EmailBackend' in .env")
        return False
    
    # Send test email
    print("\n" + "="*60)
    print("SENDING TEST EMAIL...")
    print("="*60)
    
    test_recipient = input("\nEnter test email address (default: vharadharajharshitha@gmail.com): ").strip()
    if not test_recipient:
        test_recipient = "vharadharajharshitha@gmail.com"
    
    try:
        send_mail(
            subject='🔧 SMTP Test - Agnivridhi CRM',
            message='This is a test email to verify SMTP settings are working correctly.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_recipient],
            fail_silently=False,
        )
        print(f"\n✅ SUCCESS! Test email sent to {test_recipient}")
        print("   Check the inbox (and spam folder) for the test email.")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: Failed to send test email")
        print(f"   Error message: {str(e)}")
        print("\n🔍 TROUBLESHOOTING:")
        print("   1. Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env")
        print("   2. Check if SMTP server is accessible: smtp.hostinger.com:587")
        print("   3. Ensure EMAIL_USE_TLS=True for Hostinger SMTP")
        print("   4. Check if the email account is active and not blocked")
        return False

if __name__ == '__main__':
    test_smtp_configuration()
