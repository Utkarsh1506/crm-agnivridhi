"""
Admin Dashboard Navigation Links Test
Tests all navigation links from admin dashboard to verify they work
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.test import Client
from accounts.models import User

print("\n" + "="*80)
print("  ADMIN DASHBOARD - NAVIGATION LINKS TEST")
print("="*80 + "\n")

# Create test client and login as admin
client = Client()
admin_user = User.objects.get(username='admin')
client.force_login(admin_user)

# Define all navigation links from admin dashboard
nav_links = [
    ('Dashboard', '/dashboard/admin/'),
    ('Reports & Analytics', '/reports/'),
    ('Clients', '/clients/admin/'),
    ('Bookings', '/bookings/team/'),
    ('Applications', '/applications/team/'),
    ('Schemes', '/schemes/'),
    ('Payments', '/payments/team/'),
    ('Edit Requests', '/edit-requests/manager/'),
    ('Documents', '/documents/team/'),
    ('Users', '/users/'),
    ('Notifications', '/notifications/'),
    ('Activity Feed', '/activity/'),
    ('Django Admin', '/admin/'),
]

print("Testing all navigation links...\n")
print(f"{'Link Name':<25} {'URL':<35} {'Status':<10} {'Result'}")
print("-" * 80)

success_count = 0
total_count = len(nav_links)

for name, url in nav_links:
    try:
        response = client.get(url)
        status = response.status_code
        
        if status == 200:
            result = "✓ OK"
            success_count += 1
        elif status == 302:
            result = "✓ Redirect"
            success_count += 1
        elif status == 404:
            result = "✗ NOT FOUND"
        elif status == 403:
            result = "✗ FORBIDDEN"
        elif status == 500:
            result = "✗ SERVER ERROR"
        else:
            result = f"? {status}"
        
        print(f"{name:<25} {url:<35} {status:<10} {result}")
        
    except Exception as e:
        print(f"{name:<25} {url:<35} {'ERROR':<10} ✗ {str(e)[:30]}")

print("-" * 80)
print(f"\nResults: {success_count}/{total_count} links working")

if success_count == total_count:
    print("\n✅ ALL NAVIGATION LINKS WORKING!")
else:
    print(f"\n⚠️  {total_count - success_count} link(s) have issues")

# Test common URL patterns that might be used
print("\n" + "="*80)
print("  TESTING COMMON URL PATTERNS")
print("="*80 + "\n")

common_urls = [
    ('Home/Root', '/'),
    ('Login', '/login/'),
    ('Logout', '/logout/'),
    ('Admin Dashboard', '/dashboard/admin/'),
    ('Manager Dashboard', '/dashboard/manager/'),
    ('Sales Dashboard', '/sales/dashboard/'),
    ('Client Dashboard', '/clients/dashboard/'),
    ('Clients List', '/clients/'),
    ('Schemes List', '/schemes/'),
    ('Bookings List', '/bookings/'),
    ('Applications List', '/applications/'),
    ('Payments List', '/payments/'),
]

print(f"{'URL Name':<25} {'URL':<35} {'Status':<10} {'Result'}")
print("-" * 80)

for name, url in common_urls:
    try:
        response = client.get(url)
        status = response.status_code
        
        if status in [200, 302]:
            result = "✓ OK"
        elif status == 404:
            result = "✗ NOT FOUND"
        else:
            result = f"? {status}"
        
        print(f"{name:<25} {url:<35} {status:<10} {result}")
        
    except Exception as e:
        print(f"{name:<25} {url:<35} {'ERROR':<10} ✗ ERROR")

print("\n" + "="*80)
print("Test completed!")
print("="*80 + "\n")
