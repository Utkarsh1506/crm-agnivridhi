"""
Quick Password Reset Tool - Agnivridhi CRM
Use this to reset passwords for any user

Usage:
    python reset_password.py
"""

import os
import django
import getpass

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from accounts.models import User

def reset_password():
    print("\n" + "="*70)
    print("  PASSWORD RESET TOOL - Agnivridhi CRM")
    print("="*70 + "\n")
    
    # Show available users
    print("Available Users:")
    print("-" * 70)
    users = User.objects.all().order_by('role', 'username')
    for i, user in enumerate(users, 1):
        print(f"{i:2}. {user.username:15} | {user.role:10} | {user.email}")
    print("-" * 70)
    
    # Get username
    username = input("\nEnter username to reset password: ").strip()
    
    try:
        user = User.objects.get(username=username)
        print(f"\n✓ Found user: {user.username} ({user.role})")
        print(f"  Email: {user.email}")
        
        # Get new password
        print("\n" + "-"*70)
        new_password = input("Enter new password: ").strip()
        
        if len(new_password) < 6:
            print("\n⚠  Password too short! Use at least 6 characters.")
            return
        
        # Confirm password
        confirm = input("Confirm password: ").strip()
        
        if new_password != confirm:
            print("\n✗ Passwords don't match!")
            return
        
        # Set password
        user.set_password(new_password)
        user.save()
        
        print("\n" + "="*70)
        print("✓ PASSWORD RESET SUCCESSFUL!")
        print("="*70)
        print(f"\nUser: {user.username}")
        print(f"New Password: {new_password}")
        print(f"Role: {user.role}")
        print(f"\nYou can now login with these credentials at:")
        print(f"  → http://127.0.0.1:8000/login/")
        print("\n" + "="*70 + "\n")
        
    except User.DoesNotExist:
        print(f"\n✗ User '{username}' not found!")
        print("Please check the username and try again.")
    except Exception as e:
        print(f"\n✗ Error: {e}")

def quick_reset_all():
    """Reset all users to default passwords"""
    print("\n" + "="*70)
    print("  RESET ALL USERS TO DEFAULT PASSWORDS")
    print("="*70 + "\n")
    
    confirm = input("This will reset ALL user passwords. Continue? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("\n✗ Cancelled.")
        return
    
    default_passwords = {
        'ADMIN': 'Admin@123',
        'MANAGER': 'Manager@123',
        'SALES': 'Sales@123',
        'CLIENT': 'Client@123',
        'owner': 'Owner@123',
    }
    
    users = User.objects.all()
    reset_count = 0
    
    print("\nResetting passwords...")
    print("-" * 70)
    
    for user in users:
        if user.role.upper() in default_passwords:
            password = default_passwords[user.role.upper()]
        elif user.username == 'owner':
            password = 'Owner@123'
        else:
            password = f"{user.role.capitalize()}@123"
        
        user.set_password(password)
        user.save()
        print(f"✓ {user.username:15} → {password}")
        reset_count += 1
    
    print("-" * 70)
    print(f"\n✓ Reset {reset_count} user passwords!")
    print("\nDefault passwords:")
    for role, pwd in default_passwords.items():
        print(f"  {role:10}: {pwd}")
    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    print("\n1. Reset single user password")
    print("2. Reset ALL users to default passwords")
    print("3. Exit")
    
    choice = input("\nSelect option (1/2/3): ").strip()
    
    if choice == '1':
        reset_password()
    elif choice == '2':
        quick_reset_all()
    else:
        print("\nGoodbye!")
