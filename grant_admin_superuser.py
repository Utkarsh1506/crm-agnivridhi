"""
Script to grant superuser permissions to all ADMIN role users
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from accounts.models import User

def grant_admin_superuser_permissions():
    """Grant superuser permissions to all ADMIN and OWNER role users"""
    
    print("\n" + "="*60)
    print("GRANTING SUPERUSER PERMISSIONS TO ADMIN USERS")
    print("="*60 + "\n")
    
    # Find all ADMIN and OWNER users
    admin_users = User.objects.filter(role__in=['ADMIN', 'OWNER', 'admin', 'owner'])
    
    if not admin_users.exists():
        print("❌ No ADMIN or OWNER users found in the database.")
        return
    
    print(f"Found {admin_users.count()} ADMIN/OWNER users:\n")
    
    updated_count = 0
    for user in admin_users:
        old_superuser = user.is_superuser
        old_staff = user.is_staff
        
        # Update permissions
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        # Refresh from database to confirm changes
        user.refresh_from_db()
        
        status = "✅ UPDATED" if not old_superuser else "✓ Already had permissions"
        print(f"{status} - {user.username}")
        print(f"   Role: {user.role}")
        print(f"   Email: {user.email}")
        print(f"   is_superuser: {old_superuser} → {user.is_superuser}")
        print(f"   is_staff: {old_staff} → {user.is_staff}")
        print()
        
        if not old_superuser:
            updated_count += 1
    
    print("="*60)
    print(f"✅ Successfully updated {updated_count} user(s)")
    print(f"✓ All {admin_users.count()} ADMIN/OWNER users now have superuser permissions")
    print("="*60 + "\n")
    
    print("🔑 ADMIN users can now:")
    print("   - Access Django admin panel at /admin/")
    print("   - Manage all users and data")
    print("   - Approve edit requests")
    print("   - Full system access like superusers")
    print()

if __name__ == '__main__':
    grant_admin_superuser_permissions()
