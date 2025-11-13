"""
Quick Login Test - Verify passwords work
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from django.contrib.auth import authenticate
from accounts.models import User

print("\n" + "="*70)
print("  LOGIN AUTHENTICATION TEST")
print("="*70 + "\n")

test_users = [
    ('admin', 'Admin@123', 'ADMIN'),
    ('manager1', 'Manager@123', 'MANAGER'),
    ('sales1', 'Sales@123', 'SALES'),
    ('client1', 'Client@123', 'CLIENT'),
    ('owner', 'Owner@123', 'OWNER'),
]

print("Testing login for all roles...\n")
success_count = 0

for username, password, expected_role in test_users:
    user = authenticate(username=username, password=password)
    
    if user:
        print(f"✓ {username:12} | Password: {password:15} | Role: {user.role:10} | LOGIN SUCCESS")
        success_count += 1
    else:
        print(f"✗ {username:12} | Password: {password:15} | FAILED - Wrong credentials")

print("\n" + "="*70)
print(f"Results: {success_count}/{len(test_users)} successful logins")
print("="*70 + "\n")

if success_count == len(test_users):
    print("🎉 ALL CREDENTIALS WORKING! Ready to login via browser.")
    print("\nGo to: http://127.0.0.1:8000/login/")
    print("Start with: admin / Admin@123")
else:
    print("⚠ Some logins failed. Check the output above.")

print()
