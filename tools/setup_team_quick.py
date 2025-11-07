"""
Quick Company Structure Setup - Simplified
Creates 3 managers with 3 sales employees each
"""
from accounts.models import User
from clients.models import Client
from bookings.models import Booking
from schemes.models import Scheme
from decimal import Decimal
import random

print("\n" + "="*80)
print("COMPANY STRUCTURE SETUP - SIMPLIFIED")
print("="*80)

# Create/Update Managers
print("\n[1/3] Managers...")
managers_data = [
    ('manager1', 'Rajesh', 'Kumar'),
    ('manager2', 'Priya', 'Sharma'),
    ('manager3', 'Amit', 'Patel'),
]

managers = []
for username, first, last in managers_data:
    user, created = User.objects.update_or_create(
        username=username,
        defaults={
            'first_name': first,
            'last_name': last,
            'email': f'{username}@agnivridhiindia.com',
            'role': 'MANAGER',
            'is_staff': True,
            'is_active': True,
        }
    )
    if created:
        user.set_password('test123')
        user.save()
    managers.append(user)
    print(f"  ✓ {first} {last} ({username})")

# Create/Update Sales Employees
print("\n[2/3] Sales Employees...")
sales_data = [
    # Manager 1 team
    ('sales1', 'Sales', 'One', 0),
    ('sales2', 'Neha', 'Gupta', 0),
    ('sales3', 'Rohit', 'Singh', 0),
    # Manager 2 team
    ('sales4', 'Anjali', 'Verma', 1),
    ('sales5', 'Vikram', 'Reddy', 1),
    ('sales6', 'Pooja', 'Nair', 1),
    # Manager 3 team
    ('sales7', 'Karan', 'Malhotra', 2),
    ('sales8', 'Divya', 'Iyer', 2),
    ('sales9', 'Arjun', 'Kapoor', 2),
]

sales_users = []
for username, first, last, mgr_idx in sales_data:
    user, created = User.objects.update_or_create(
        username=username,
        defaults={
            'first_name': first,
            'last_name': last,
            'email': f'{username}@agnivridhiindia.com',
            'role': 'SALES',
            'manager': managers[mgr_idx],
            'is_staff': False,
            'is_active': True,
        }
    )
    if created:
        user.set_password('test123')
        user.save()
    sales_users.append(user)
    print(f"  ✓ {first} {last} ({username}) → {managers[mgr_idx].get_full_name()}")

# Show Team Structure
print("\n[3/3] Team Structure...")
for i, manager in enumerate(managers, 1):
    team = User.objects.filter(role='SALES', manager=manager)
    print(f"\n  Manager {i}: {manager.get_full_name()}")
    for sales in team:
        client_count = Client.objects.filter(assigned_sales=sales).count()
        print(f"    ├─ {sales.get_full_name()}: {client_count} clients")

print("\n" + "="*80)
print("✅ COMPLETE - All managers and sales employees ready!")
print(f"   Password for all: test123")
print("="*80 + "\n")
