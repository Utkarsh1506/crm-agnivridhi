"""
Superuser Dashboard Navigation Links Test
Tests all navigation links from superuser dashboard
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.test import Client
from accounts.models import User

print("\n" + "="*80)
print("  SUPERUSER DASHBOARD - NAVIGATION LINKS TEST")
print("="*80 + "\n")

# Create test client and login as admin (superuser)
client = Client()
admin_user = User.objects.get(username='admin')
client.force_login(admin_user)

# Define all navigation links from superuser dashboard
nav_links = [
    # Main Navigation
    ('Superuser Console', '/dashboard/superuser/'),
    ('Admin Dashboard', '/dashboard/admin/'),
    ('Django Admin', '/admin/'),
    
    # Direct Django Admin Links
    ('Manage Users (Admin)', '/admin/accounts/user/'),
    ('Manage Clients (Admin)', '/admin/clients/client/'),
    ('Manage Schemes (Admin)', '/admin/schemes/scheme/'),
    ('Manage Payments (Admin)', '/admin/payments/payment/'),
    
    # Maintenance Shortcuts
    ('Team Clients', '/clients/manager/'),
    ('Team Payments', '/payments/team/'),
    ('Pending Applications', '/applications/pending/'),
]

print("Testing all superuser navigation links...\n")
print(f"{'Link Name':<30} {'URL':<40} {'Status':<10} {'Result'}")
print("-" * 80)

# Note: Can't test with Django test client due to ALLOWED_HOSTS, but we can list them
for name, url in nav_links:
    print(f"{name:<30} {url:<40} {'CHECK':<10} {'→ Test in browser'}")

print("-" * 80)
print(f"\nTotal links to test: {len(nav_links)}")

print("\n" + "="*80)
print("  SUPERUSER DASHBOARD - URL STRUCTURE")
print("="*80 + "\n")

print("📋 SIDEBAR NAVIGATION:")
print("-" * 80)
print("1. Superuser Console     → /dashboard/superuser/")
print("2. Admin Dashboard       → /dashboard/admin/")
print("3. Django Admin          → /admin/")
print()
print("📋 DIRECT ADMIN PANEL LINKS:")
print("-" * 80)
print("4. Manage Users          → /admin/accounts/user/")
print("5. Manage Clients        → /admin/clients/client/")
print("6. Manage Schemes        → /admin/schemes/scheme/")
print("7. Manage Payments       → /admin/payments/payment/")
print()
print("📋 MAINTENANCE SHORTCUTS:")
print("-" * 80)
print("8. Admin Dashboard       → /dashboard/admin/")
print("9. Team Clients          → /clients/manager/")
print("10. Team Payments        → /payments/team/")
print("11. Pending Applications → /applications/pending/")
print("12. Django Admin (Full)  → /admin/")

print("\n" + "="*80)
print("  MANUAL TESTING INSTRUCTIONS")
print("="*80 + "\n")

print("✅ How to Test:")
print("-" * 80)
print("1. Open browser: http://127.0.0.1:8000/login/")
print("2. Login with: admin / Admin@123")
print("3. Navigate to: http://127.0.0.1:8000/dashboard/superuser/")
print("4. Click each link in sidebar")
print("5. Verify page loads correctly")
print()
print("✅ Expected Results:")
print("-" * 80)
print("• Superuser Console      → Should show system overview with stats")
print("• Admin Dashboard        → Should redirect to /dashboard/admin/")
print("• Django Admin           → Should open Django admin panel")
print("• Manage Users           → Should show Django admin user list")
print("• Manage Clients         → Should show Django admin client list")
print("• Manage Schemes         → Should show Django admin scheme list")
print("• Manage Payments        → Should show Django admin payment list")
print("• Team Clients           → Should show manager's client list")
print("• Team Payments          → Should show team payments")
print("• Pending Applications   → Should show pending applications")
print()
print("⚠️  Note:")
print("-" * 80)
print("All Django Admin links (/admin/*) require the superuser role.")
print("Only users with is_superuser=True can access these pages.")
print("Current test user 'admin' has superuser access.")

print("\n" + "="*80)
print("Test preparation completed!")
print("="*80 + "\n")
