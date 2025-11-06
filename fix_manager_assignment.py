import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from accounts.models import User

print("Assigning sales1 to manager1...")

try:
    sales1 = User.objects.get(username='sales1')
    manager1 = User.objects.get(username='manager1')
    
    print(f"Found: {sales1.username} (currently manager: {sales1.manager})")
    print(f"Found: {manager1.username}")
    
    sales1.manager = manager1
    sales1.save()
    
    print(f"\n✅ SUCCESS! {sales1.username} is now assigned to {manager1.username}")
    print(f"Verification: {sales1.username}.manager = {sales1.manager.username}")
    
except User.DoesNotExist as e:
    print(f"❌ ERROR: User not found - {e}")
except Exception as e:
    print(f"❌ ERROR: {e}")
