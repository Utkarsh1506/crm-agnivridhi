"""
Create Test Users for All Roles - Agnivridhi CRM
Run this on PythonAnywhere to create test users for testing

Usage:
    cd ~/crm-agnivridhi
    workon crm-env
    python create_test_users.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from accounts.models import User
from django.db import IntegrityError

def create_test_users():
    """Create test users for all roles"""
    
    test_users = [
        {
            'username': 'admin',
            'email': 'admin@agnivridhiindia.com',
            'password': 'Admin@123',
            'role': 'ADMIN',
            'first_name': 'Admin',
            'last_name': 'User',
            'phone': '9999999991',
            'is_staff': True,
            'is_superuser': False,
        },
        {
            'username': 'manager',
            'email': 'manager@agnivridhiindia.com',
            'password': 'Manager@123',
            'role': 'MANAGER',
            'first_name': 'Manager',
            'last_name': 'User',
            'phone': '9999999992',
            'is_staff': True,
            'is_superuser': False,
        },
        {
            'username': 'sales',
            'email': 'sales@agnivridhiindia.com',
            'password': 'Sales@123',
            'role': 'SALES',
            'first_name': 'Sales',
            'last_name': 'User',
            'phone': '9999999993',
            'is_staff': True,
            'is_superuser': False,
        },
        {
            'username': 'client',
            'email': 'client@example.com',
            'password': 'Client@123',
            'role': 'CLIENT',
            'first_name': 'Test',
            'last_name': 'Client',
            'phone': '9999999994',
            'is_staff': False,
            'is_superuser': False,
        },
        {
            'username': 'owner',
            'email': 'owner@agnivridhiindia.com',
            'password': 'Owner@123',
            'role': 'OWNER',
            'first_name': 'Owner',
            'last_name': 'Admin',
            'phone': '9999999995',
            'is_staff': True,
            'is_superuser': False,
            'is_owner': True,  # Special flag for owner
        },
    ]
    
    print("=" * 60)
    print("Creating Test Users for Agnivridhi CRM")
    print("=" * 60)
    print()
    
    created_count = 0
    existing_count = 0
    
    for user_data in test_users:
        # Avoid passing duplicate 'username' to create_user
        username = user_data.pop('username')
        password = user_data.pop('password')
        
        try:
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                print(f"⚠  User '{username}' already exists - skipping")
                existing_count += 1
                continue
            
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                **user_data
            )
            
            print(f"✓ Created: {username:12} | Role: {user.role:8} | Email: {user.email}")
            created_count += 1
            
        except IntegrityError as e:
            print(f"✗ Error creating '{username}': {e}")
        except Exception as e:
            print(f"✗ Unexpected error for '{username}': {e}")
    
    print()
    print("=" * 60)
    print(f"Summary: {created_count} created, {existing_count} already existed")
    print("=" * 60)
    print()
    
    if created_count > 0:
        print("✓ Test users created successfully!")
        print()
        print("You can now login with these credentials:")
        print()


if __name__ == '__main__':
    create_test_users()
    
    # Display credentials
    print("-" * 60)
    print("TEST USER CREDENTIALS")
    print("-" * 60)
    print()
    print("1. ADMIN USER")
    print("   Username: admin")
    print("   Password: Admin@123")
    print("   Role: ADMIN")
    print("   Access: Full admin dashboard, manage users, schemes, etc.")
    print()
    print("2. MANAGER USER")
    print("   Username: manager")
    print("   Password: Manager@123")
    print("   Role: MANAGER")
    print("   Access: Manage applications, bookings, assign tasks")
    print()
    print("3. SALES USER")
    print("   Username: sales")
    print("   Password: Sales@123")
    print("   Role: SALES")
    print("   Access: Create bookings, manage clients, track leads")
    print()
    print("4. CLIENT USER")
    print("   Username: client")
    print("   Password: Client@123")
    print("   Role: CLIENT")
    print("   Access: Client portal, view own applications, payments")
    print()
    print("5. OWNER USER")
    print("   Username: owner")
    print("   Password: Owner@123")
    print("   Role: OWNER")
    print("   Access: Full system access, analytics, reports")
    print()
    print("-" * 60)
    print()
    print("🔗 Login URL: https://agnivridhicrm.pythonanywhere.com/login/")
    print()
    print("⚠  IMPORTANT: Change these passwords after testing!")
    print("-" * 60)
