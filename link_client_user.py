#!/usr/bin/env python
"""
Link client user to client profile
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from accounts.models import User
from clients.models import Client

def link_client_user():
    """Link client user to client profile"""
    
    # Get client user
    client_user = User.objects.filter(role='CLIENT').first()
    if not client_user:
        print("❌ No CLIENT user found. Creating one...")
        client_user = User.objects.create_user(
            username='client1',
            email='client1@agnivridhiindia.com',
            password='Client@123',
            role='CLIENT',
            first_name='Test',
            last_name='Client'
        )
        print(f"✅ Created client user: {client_user.email}")
    else:
        print(f"✅ Found client user: {client_user.email}")
    
    # Get client profile
    client = Client.objects.first()
    if not client:
        print("❌ No client profile found in database.")
        return
    
    print(f"✅ Found client profile: {client.company_name}")
    
    # Check if already linked
    if client.user:
        print(f"⚠️  Client already linked to user: {client.user.email}")
        if client.user != client_user:
            print(f"   Updating link from {client.user.email} to {client_user.email}")
            client.user = client_user
            client.save()
            print(f"✅ Updated link!")
        else:
            print(f"✅ Already correctly linked!")
    else:
        print(f"📎 Linking client profile to user...")
        client.user = client_user
        client.save()
        print(f"✅ Successfully linked {client.company_name} to {client_user.email}")
    
    print(f"\n🎯 Client can now login with:")
    print(f"   Email: {client_user.email}")
    print(f"   Password: Client@123")
    print(f"   Dashboard: http://127.0.0.1:8000/tracking/dashboard/")

if __name__ == '__main__':
    link_client_user()
