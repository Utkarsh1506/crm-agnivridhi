#!/usr/bin/env python
"""
Email Configuration Test Script
Run this on PythonAnywhere to diagnose OTP email issues
Usage: python test_email_config.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail
from accounts.clerk_auth import clerk_service

def print_separator(title=""):
    print("\n" + "="*60)
    if title:
        print(f"  {title}")
        print("="*60)

def test_email_settings():
    """Check Django email settings"""
    print_separator("1. EMAIL SETTINGS CHECK")
    
    print(f"Backend: {settings.EMAIL_BACKEND}")
    print(f"Host: {settings.EMAIL_HOST}")
    print(f"Port: {settings.EMAIL_PORT}")
    print(f"Use TLS: {settings.EMAIL_USE_TLS}")
    print(f"Username: {settings.EMAIL_HOST_USER}")
    print(f"Password: {'*' * min(len(settings.EMAIL_HOST_PASSWORD), 10) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
    print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")
    print(f"Timeout: {settings.EMAIL_TIMEOUT}s")
    
    if not settings.EMAIL_HOST_PASSWORD:
        print("\n[WARNING] EMAIL_HOST_PASSWORD is not set!")
        return False
    
    print("\n[OK] Email settings configured")
    return True

def test_smtp_connection():
    """Test SMTP connection"""
    print_separator("2. SMTP CONNECTION TEST")
    
    try:
        from smtplib import SMTP
        
        print(f"Connecting to {settings.EMAIL_HOST}:{settings.EMAIL_PORT}...")
        
        with SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10) as smtp:
            print("[OK] Connection established")
            
            if settings.EMAIL_USE_TLS:
                print("Starting TLS...")
                smtp.starttls()
                print("[OK] TLS started")
            
            print("Authenticating...")
            smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            print("[OK] Authentication successful")
        
        print("\n[SUCCESS] SMTP connection test passed!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] SMTP connection failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

def test_django_email():
    """Test Django send_mail function"""
    print_separator("3. DJANGO EMAIL TEST")
    
    test_email = input("Enter test email address (press Enter for default): ").strip()
    if not test_email:
        test_email = "testclient@agnivridhi.com"
    
    print(f"Sending test email to: {test_email}")
    
    try:
        result = send_mail(
            subject='Test Email - Agnivridhi CRM OTP System',
            message='This is a test email to verify SMTP configuration for OTP delivery.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        print(f"[OK] Email sent successfully! (result: {result})")
        print(f"\nCheck inbox (and spam folder) at: {test_email}")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Failed to send email: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("\nFull traceback:")
        print(traceback.format_exc())
        return False

def test_otp_service():
    """Test OTP service"""
    print_separator("4. OTP SERVICE TEST")
    
    test_email = input("Enter test email address (press Enter for default): ").strip()
    if not test_email:
        test_email = "testclient@agnivridhi.com"
    
    print(f"Testing OTP service for: {test_email}")
    
    try:
        result = clerk_service.send_otp(test_email)
        
        print(f"\nSuccess: {result['success']}")
        print(f"Message: {result['message']}")
        
        if result.get('otp'):
            print(f"OTP Code: {result['otp']}")
        
        if result['success']:
            print("\n[SUCCESS] OTP service test passed!")
            print(f"Check inbox at: {test_email}")
        else:
            print("\n[FAILED] OTP service test failed!")
        
        return result['success']
        
    except Exception as e:
        print(f"\n[ERROR] OTP service error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

def main():
    print("="*60)
    print("  AGNIVRIDHI CRM - OTP EMAIL TROUBLESHOOTER")
    print("="*60)
    
    results = {
        'settings': False,
        'smtp': False,
        'django_email': False,
        'otp_service': False
    }
    
    # Test 1: Check settings
    results['settings'] = test_email_settings()
    
    if not results['settings']:
        print("\n[ABORT] Cannot proceed without proper email settings")
        return
    
    # Test 2: SMTP connection
    results['smtp'] = test_smtp_connection()
    
    # Test 3: Django email
    if results['smtp']:
        results['django_email'] = test_django_email()
    else:
        print("\n[SKIP] Skipping Django email test due to SMTP failure")
    
    # Test 4: OTP service
    if results['django_email']:
        results['otp_service'] = test_otp_service()
    else:
        print("\n[SKIP] Skipping OTP service test due to email failure")
    
    # Summary
    print_separator("TEST SUMMARY")
    print(f"1. Email Settings: {'PASS' if results['settings'] else 'FAIL'}")
    print(f"2. SMTP Connection: {'PASS' if results['smtp'] else 'FAIL'}")
    print(f"3. Django Email: {'PASS' if results['django_email'] else 'FAIL'}")
    print(f"4. OTP Service: {'PASS' if results['otp_service'] else 'FAIL'}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("  ALL TESTS PASSED!")
        print("  OTP email system is working correctly.")
    else:
        print("  SOME TESTS FAILED!")
        print("  Check error messages above for details.")
    print("="*60)
    
    # Recommendations
    if not results['smtp']:
        print("\nRECOMMENDATIONS:")
        print("- Check if SMTP port 587 is allowed on your server")
        print("- Verify email credentials are correct")
        print("- Check firewall/security settings")
        print("- Try using console backend for testing:")
        print("  EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'")

if __name__ == '__main__':
    main()
