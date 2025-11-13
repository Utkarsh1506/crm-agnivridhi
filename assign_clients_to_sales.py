#!/usr/bin/env python
"""
Assign clients to sales users for testing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from accounts.models import User
from clients.models import Client

def assign_clients_to_sales():
    """Assign clients to sales users"""
    
    # Get sales users
    sales_users = User.objects.filter(role='SALES')[:3]
    if not sales_users:
        print("❌ No SALES users found.")
        return
    
    # Get all clients
    clients = Client.objects.all()
    if not clients:
        print("❌ No clients found in database.")
        return
    
    print(f"✅ Found {sales_users.count()} sales users")
    print(f"✅ Found {clients.count()} clients")
    print("\n📋 Assigning clients to sales users...\n")
    
    # Assign clients to sales users in round-robin fashion
    for i, client in enumerate(clients):
        sales_user = sales_users[i % len(sales_users)]
        client.assigned_sales = sales_user
        client.save()
        print(f"  ✅ {client.company_name} → {sales_user.first_name} {sales_user.last_name} ({sales_user.email})")
    
    print(f"\n✅ All clients assigned!")
    
    # Show summary
    print(f"\n📊 Assignment Summary:")
    for sales in sales_users:
        assigned_count = Client.objects.filter(assigned_sales=sales).count()
        print(f"   {sales.first_name} {sales.last_name}: {assigned_count} clients")

if __name__ == '__main__':
    assign_clients_to_sales()
