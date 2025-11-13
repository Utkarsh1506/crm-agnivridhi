import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from clients.models import Client
from django.contrib.auth import get_user_model

User = get_user_model()

# Find all managers
managers = User.objects.filter(role='MANAGER')
print(f'Total Managers: {managers.count()}\n')

for manager in managers:
    print(f'Manager: {manager.get_full_name()} ({manager.username})')
    
    # Check clients created by this manager
    created_clients = Client.objects.filter(created_by=manager)
    print(f'  Created by this manager: {created_clients.count()}')
    for c in created_clients[:2]:
        print(f'    - {c.company_name}, assigned_manager={c.assigned_manager}, assigned_sales={c.assigned_sales}')
    
    # Check clients assigned to this manager
    assigned_clients = Client.objects.filter(assigned_manager=manager)
    print(f'  Assigned to this manager: {assigned_clients.count()}')
    for c in assigned_clients[:2]:
        print(f'    - {c.company_name}, created_by={c.created_by}')
    print()
