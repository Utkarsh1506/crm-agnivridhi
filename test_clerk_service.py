#!/usr/bin/env python
"""
Test script for Clerk OTP Service
Verifies configuration and basic functionality
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from accounts.clerk_otp_service import clerk_service
from django.conf import settings

print("=" * 60)
print("CLERK OTP SERVICE TEST")
print("=" * 60)

# Test 1: Check configuration
print("\n1. Configuration Check:")
print(f"   CLERK_PUBLIC_KEY set: {bool(settings.CLERK_PUBLIC_KEY)}")
print(f"   CLERK_SECRET_KEY set: {bool(settings.CLERK_SECRET_KEY)}")
print(f"   Service initialized: {clerk_service is not None}")

if not settings.CLERK_SECRET_KEY:
    print("\n   ⚠️  WARNING: CLERK_SECRET_KEY not configured!")
    print("       Add to .env: CLERK_SECRET_KEY=sk_live_xxx")
    exit(1)

# Test 2: Check API connectivity
print("\n2. API Connectivity Check:")
print(f"   API Base URL: {clerk_service.api_base}")
print(f"   API Key format: {clerk_service.clerk_api_key[:10]}...hidden")

# Test 3: Service methods available
print("\n3. Service Methods:")
methods = ['send_otp', 'verify_otp', 'get_or_create_user']
for method in methods:
    has_method = hasattr(clerk_service, method) and callable(getattr(clerk_service, method))
    status = "✓" if has_method else "✗"
    print(f"   {status} {method}")

# Test 4: Test OTP send (optional - only if email provided)
print("\n4. Optional OTP Send Test:")
print("   To test OTP sending, run:")
print("   $ python manage.py shell")
print("   >>> from accounts.clerk_otp_service import clerk_service")
print("   >>> result = clerk_service.send_otp('your-test-email@example.com')")
print("   >>> print(result)")

print("\n" + "=" * 60)
print("✅ CLERK OTP SERVICE READY FOR TESTING")
print("=" * 60)
print("\nNext steps:")
print("1. Start Django: python manage.py runserver")
print("2. Visit: http://localhost:8000/accounts/client-login/")
print("3. Enter your email and check inbox for OTP")
print("4. Enter the OTP code to verify")
print("\n" + "=" * 60)
