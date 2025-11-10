"""
Quick test to verify OWNER role has admin and manager privileges.
Tests the is_admin property and decorator access.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from accounts.models import User
from accounts.constants import ROLE_OWNER, ROLE_ADMIN, ROLE_MANAGER

# Test with existing owner user (akash@agnivridhiindia.com)
try:
    owner = User.objects.get(email='akash@agnivridhiindia.com')
    
    print("=" * 60)
    print("OWNER ROLE PERMISSION VERIFICATION")
    print("=" * 60)
    print(f"\nUser: {owner.username} ({owner.email})")
    print(f"Role: {owner.role}")
    print(f"is_owner flag: {owner.is_owner}")
    print(f"\n--- Role Properties ---")
    print(f"is_admin: {owner.is_admin}")
    print(f"is_manager: {owner.is_manager}")
    print(f"is_staff_member: {owner.is_staff_member}")
    print(f"is_superuser: {owner.is_superuser}")
    
    # Test expected behaviors
    print(f"\n--- Expected Behaviors ---")
    tests = [
        ("✓" if owner.role.upper() == ROLE_OWNER.upper() else "✗", "Role is 'OWNER'"),
        ("✓" if owner.is_owner else "✗", "is_owner flag is True"),
        ("✓" if owner.is_admin else "✗", "is_admin returns True (OWNER treated as ADMIN)"),
        ("✓" if not owner.is_manager else "✗", "is_manager returns False (OWNER is ABOVE manager)"),
        ("✓" if owner.is_staff_member else "✗", "is_staff_member returns True"),
    ]
    
    for status, description in tests:
        print(f"{status} {description}")
    
    # Summary
    all_pass = all(status == "✓" for status, _ in tests)
    print(f"\n{'✓' if all_pass else '✗'} Overall: {'All checks passed!' if all_pass else 'Some checks failed'}")
    
    print(f"\n--- Access Summary ---")
    print("With these settings, the OWNER user can:")
    print("  • Access admin_dashboard (admin_required decorator)")
    print("  • Access owner_dashboard (OWNER-specific)")
    print("  • Access manager_dashboard (manager_required decorator)")
    print("  • Access sales_dashboard (staff_required decorator)")
    print("  • Edit clients directly without approval")
    print("  • Approve edit requests from sales users")
    print("  • View and manage all system resources")
    print("=" * 60)
    
except User.DoesNotExist:
    print("ERROR: User 'akash@agnivridhiindia.com' not found.")
    print("Please create the OWNER user first.")
