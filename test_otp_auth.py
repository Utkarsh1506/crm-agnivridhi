#!/usr/bin/env python
"""
Test script for Clerk OTP authentication
Creates a test client and tests the OTP login flow
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from accounts.models import User  # Use custom User model from accounts
from clients.models import Client
from accounts.clerk_auth import clerk_service
from django.core.cache import cache

print("\n" + "="*60)
print("🧪 CLERK OTP AUTHENTICATION - LOCAL TEST")
print("="*60)

# Step 1: Create test user
print("\n📝 Step 1: Creating test user...")
user, created = User.objects.get_or_create(
    username='testclient',
    defaults={
        'email': 'testclient@agnivridhi.com',
        'first_name': 'Test',
        'last_name': 'Client'
    }
)
print(f"✓ User: {user.username} ({user.email})")

# Step 2: Create test client
print("\n📝 Step 2: Creating test client...")
client, created = Client.objects.get_or_create(
    user=user,
    defaults={
        'company_name': 'Test Company Ltd',
        'contact_email': 'testclient@agnivridhi.com',
        'is_approved': False,
        'business_type': 'PVT_LTD',
        'sector': 'SERVICE',
        'status': 'ACTIVE'
    }
)
print(f"✓ Client: {client.company_name}")
print(f"  Email: {client.contact_email}")
print(f"  Status: {'Approved ✅' if client.is_approved else 'Pending ⏳'}")

# Step 3: Approve client (triggers welcome email signal)
print("\n🔔 Step 3: Approving client (auto-sends welcome email)...")
client.is_approved = True
client.approved_by = User.objects.filter(is_staff=True).first() or user
client.save()
print(f"✓ Client approved!")
print(f"  → Welcome email should have been sent (check email backend)")

# Step 4: Test OTP generation
print("\n🔐 Step 4: Testing OTP generation...")
email = client.contact_email
otp_result = clerk_service.send_otp(email)
print(f"✓ OTP sent: {otp_result['message']}")
if otp_result.get('otp'):
    print(f"  📌 OTP CODE for testing: {otp_result['otp']} (DEBUG mode)")
    test_otp = otp_result['otp']
else:
    print("  ⚠️  OTP not returned (check email)")
    test_otp = None

# Step 5: Test OTP verification
print("\n✔️ Step 5: Testing OTP verification...")
if test_otp:
    verify_result = clerk_service.verify_otp(email, test_otp)
    print(f"✓ OTP verified: {verify_result['message']}")
    print(f"  Valid: {'✅ YES' if verify_result['is_valid'] else '❌ NO'}")
else:
    print("⚠️  Cannot test verification (OTP not in debug response)")

# Step 6: Display login instructions
print("\n" + "="*60)
print("📋 LOGIN TEST INSTRUCTIONS")
print("="*60)
print(f"""
1. Open browser: http://127.0.0.1:8000/accounts/client-login/

2. Enter email: {email}

3. Click "Send OTP Code"
   → Check console output for OTP code (debug mode)
   → OR check email inbox (noreply@agnivridhiindia.com)

4. Enter OTP at: http://127.0.0.1:8000/accounts/client-verify-otp/

5. ✅ You should be logged in!

═══════════════════════════════════════════════════════════
Test Credentials:
  Username: {user.username}
  Company:  {client.company_name}
  Email:    {email}
  Password: (not needed - OTP login)
═══════════════════════════════════════════════════════════
""")

# Display cache status
print("\n💾 Cache Status:")
cache_key = f"client_otp_{email}"
cached_otp = cache.get(cache_key)
if cached_otp:
    print(f"✓ OTP in cache: {'*' * len(str(cached_otp))} (hidden)")
else:
    print("⚠️  OTP not in cache or expired")

print("\n✅ Test setup complete!")
print("="*60 + "\n")
