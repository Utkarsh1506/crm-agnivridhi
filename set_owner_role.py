"""
Update Akash's role from ADMIN to OWNER
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from accounts.models import User
from accounts.constants import ROLE_OWNER

try:
    owner = User.objects.get(email='akash@agnivridhiindia.com')
    
    print(f"Current state:")
    print(f"  Role: {owner.role}")
    print(f"  is_owner: {owner.is_owner}")
    
    # Change role to OWNER
    owner.role = ROLE_OWNER
    owner.save()  # This will auto-set is_owner=True
    
    # Reload to confirm
    owner.refresh_from_db()
    
    print(f"\nUpdated state:")
    print(f"  Role: {owner.role}")
    print(f"  is_owner: {owner.is_owner}")
    print(f"  is_admin: {owner.is_admin}")
    print(f"  is_manager: {owner.is_manager}")
    
    print(f"\n✓ Successfully updated {owner.username} to OWNER role")
    
except User.DoesNotExist:
    print("ERROR: User 'akash@agnivridhiindia.com' not found.")
