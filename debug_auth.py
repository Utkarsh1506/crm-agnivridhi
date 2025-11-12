"""
Debug Authentication Issues - Agnivridhi CRM
Run this to diagnose login problems

Usage:
    cd ~/crm-agnivridhi
    workon crm-env
    python debug_auth.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from accounts.models import User
from django.contrib.auth import authenticate
from django.conf import settings

print("=" * 70)
print("AUTHENTICATION DEBUG - Agnivridhi CRM")
print("=" * 70)
print()

# 1. Check Database Connection
print("1. DATABASE CONNECTION")
print("-" * 70)
try:
    from django.db import connection
    connection.ensure_connection()
    print("✓ Database connection: OK")
    print(f"  Database: {settings.DATABASES['default']['NAME']}")
    print(f"  Host: {settings.DATABASES['default']['HOST']}")
except Exception as e:
    print(f"✗ Database connection: FAILED")
    print(f"  Error: {e}")
print()

# 2. Check Users Exist
print("2. USERS IN DATABASE")
print("-" * 70)
try:
    user_count = User.objects.count()
    print(f"Total users: {user_count}")
    
    if user_count == 0:
        print("⚠  NO USERS FOUND!")
        print("   You need to create users first.")
        print("   Run: python create_test_users.py")
    else:
        print("\nExisting users:")
        for user in User.objects.all()[:10]:
            role = getattr(user, 'role', 'N/A')
            print(f"  - {user.username:15} | Role: {role:10} | Active: {user.is_active}")
except Exception as e:
    print(f"✗ Error checking users: {e}")
print()

# 3. Check if 'admin' user exists
print("3. CHECK TEST ADMIN USER")
print("-" * 70)
try:
    admin_user = User.objects.filter(username='admin').first()
    if admin_user:
        print("✓ User 'admin' exists")
        print(f"  Email: {admin_user.email}")
        print(f"  Role: {getattr(admin_user, 'role', 'N/A')}")
        print(f"  Active: {admin_user.is_active}")
        print(f"  Staff: {admin_user.is_staff}")
        print(f"  Has password: {bool(admin_user.password)}")
    else:
        print("✗ User 'admin' does NOT exist")
        print("  You need to create it first!")
except Exception as e:
    print(f"✗ Error: {e}")
print()

# 4. Test Authentication
print("4. TEST AUTHENTICATION")
print("-" * 70)
test_credentials = [
    ('admin', 'Admin@123'),
    ('manager', 'Manager@123'),
    ('sales', 'Sales@123'),
]

for username, password in test_credentials:
    try:
        user = authenticate(username=username, password=password)
        if user:
            print(f"✓ {username:15} - Authentication SUCCESS")
        else:
            # Check if user exists but password is wrong
            if User.objects.filter(username=username).exists():
                print(f"✗ {username:15} - User exists but password INCORRECT")
            else:
                print(f"✗ {username:15} - User does NOT exist")
    except Exception as e:
        print(f"✗ {username:15} - Error: {e}")
print()

# 5. Check Django Settings
print("5. DJANGO SETTINGS")
print("-" * 70)
print(f"DEBUG: {settings.DEBUG}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"SECRET_KEY configured: {bool(settings.SECRET_KEY)}")
print(f"SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
print(f"CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
print()

# 6. Check AUTH_USER_MODEL
print("6. AUTHENTICATION BACKEND")
print("-" * 70)
print(f"AUTH_USER_MODEL: {settings.AUTH_USER_MODEL}")
print(f"AUTHENTICATION_BACKENDS: {settings.AUTHENTICATION_BACKENDS if hasattr(settings, 'AUTHENTICATION_BACKENDS') else 'Default'}")
print()

# 7. Recommendations
print("=" * 70)
print("RECOMMENDATIONS")
print("=" * 70)

# Check if users need to be created
if User.objects.count() == 0:
    print("\n⚠  NO USERS EXIST!")
    print("\nQuick Fix:")
    print("  python create_test_users.py")
    
# Check if admin exists but can't auth
elif User.objects.filter(username='admin').exists():
    admin = User.objects.get(username='admin')
    if not authenticate(username='admin', password='Admin@123'):
        print("\n⚠  Admin user exists but password is incorrect!")
        print("\nQuick Fix - Reset password:")
        print("  python manage.py shell")
        print("  >>> from accounts.models import User")
        print("  >>> user = User.objects.get(username='admin')")
        print("  >>> user.set_password('Admin@123')")
        print("  >>> user.save()")
        print("  >>> exit()")

# Check security settings
if settings.SESSION_COOKIE_SECURE or settings.CSRF_COOKIE_SECURE:
    print("\n⚠  Security cookies enabled but might cause issues")
    print("\nFor PythonAnywhere, try setting in .env:")
    print("  SESSION_COOKIE_SECURE=False")
    print("  CSRF_COOKIE_SECURE=False")
    print("  (PythonAnywhere already provides HTTPS)")

print()
print("=" * 70)
print("DEBUG COMPLETE")
print("=" * 70)
print()
print("Next steps:")
print("1. Fix any issues above")
print("2. Reload your web app")
print("3. Try logging in again")
print()
