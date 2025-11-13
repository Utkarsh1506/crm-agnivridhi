"""
Setup script for PythonAnywhere deployment
Creates initial users and grants appropriate permissions
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from accounts.models import User
from django.db import IntegrityError

def setup_users():
    """Create or update essential users for the system"""
    
    print("\n" + "="*60)
    print("PYTHONANYWHERE USER SETUP")
    print("="*60 + "\n")
    
    users_to_create = [
        {
            'username': 'admin',
            'email': 'admin@agnivridhiindia.com',
            'password': 'Admin@123',
            'role': 'ADMIN',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_superuser': True,
            'is_staff': True,
            'designation': 'Administrator'
        },
        {
            'username': 'owner',
            'email': 'akash@agnivridhiindia.com',
            'password': 'Owner@123',
            'role': 'OWNER',
            'first_name': 'Akash',
            'last_name': 'Gupta',
            'is_owner': True,
            'is_superuser': True,
            'is_staff': True,
            'designation': 'Owner'
        },
        {
            'username': 'manager1',
            'email': 'manager@agnivridhiindia.com',
            'password': 'Manager@123',
            'role': 'MANAGER',
            'first_name': 'Manager',
            'last_name': 'One',
            'is_staff': True,
            'designation': 'Manager',
            'employee_id': 'MGR001'
        },
        {
            'username': 'sales1',
            'email': 'sales@agnivridhiindia.com',
            'password': 'Sales@123',
            'role': 'SALES',
            'first_name': 'Sales',
            'last_name': 'One',
            'is_staff': True,
            'designation': 'Sales Executive',
            'employee_id': 'SAL001'
        },
        {
            'username': 'client1',
            'email': 'client@example.com',
            'password': 'Client@123',
            'role': 'CLIENT',
            'first_name': 'Test',
            'last_name': 'Client'
        }
    ]
    
    created = 0
    updated = 0
    
    for user_data in users_to_create:
        username = user_data.pop('username')
        password = user_data.pop('password')
        
        try:
            user, created_new = User.objects.get_or_create(
                username=username,
                defaults=user_data
            )
            
            if created_new:
                user.set_password(password)
                user.save()
                print(f"✅ CREATED: {username} ({user_data.get('role', 'N/A')})")
                print(f"   Email: {user_data.get('email')}")
                print(f"   Password: {password}")
                created += 1
            else:
                # Update existing user
                for key, value in user_data.items():
                    setattr(user, key, value)
                user.set_password(password)
                user.save()
                print(f"✅ UPDATED: {username} ({user_data.get('role', 'N/A')})")
                print(f"   Email: {user_data.get('email')}")
                print(f"   Password: {password}")
                updated += 1
            
            print()
            
        except IntegrityError as e:
            print(f"❌ ERROR creating {username}: {e}\n")
    
    print("="*60)
    print(f"✅ Setup Complete!")
    print(f"   Created: {created} users")
    print(f"   Updated: {updated} users")
    print("="*60 + "\n")
    
    # Verify admin/owner users have superuser status
    admin_users = User.objects.filter(role__in=['ADMIN', 'OWNER'])
    print(f"\n📊 Admin/Owner Users Status:")
    for user in admin_users:
        print(f"   • {user.username}: is_superuser={user.is_superuser}, is_staff={user.is_staff}")
    
    print("\n🔑 Login Credentials:")
    print("   Admin:   admin / Admin@123")
    print("   Owner:   owner / Owner@123")
    print("   Manager: manager1 / Manager@123")
    print("   Sales:   sales1 / Sales@123")
    print("   Client:  client1 / Client@123")
    print()

if __name__ == '__main__':
    setup_users()
