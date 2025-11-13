#!/usr/bin/env python
"""
Setup client profile and link to user
Creates client profile if it doesn't exist
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')
django.setup()

from accounts.models import User
from clients.models import Client

def setup_client_profile():
    """Create or link client profile"""
    
    print("🔍 Checking for CLIENT user...\n")
    
    # Get or create client user
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
    
    print(f"\n🔍 Checking for Client profile...\n")
    
    # Check if client profile exists
    client = Client.objects.filter(user=client_user).first()
    if client:
        print(f"✅ Client profile already exists: {client.company_name}")
        print(f"   Already linked to: {client.user.email}")
        return
    
    # Check if any unlinked client exists
    unlinked_client = Client.objects.filter(user__isnull=True).first()
    if unlinked_client:
        print(f"✅ Found unlinked client profile: {unlinked_client.company_name}")
        unlinked_client.user = client_user
        unlinked_client.save()
        print(f"✅ Linked to user: {client_user.email}")
        return
    
    # Get a sales user to assign
    sales_user = User.objects.filter(role='SALES').first()
    if not sales_user:
        print("⚠️  No SALES user found. Client will be created without sales assignment.")
    else:
        print(f"✅ Found sales user for assignment: {sales_user.email}")
    
    # Create new client profile
    print(f"\n📝 Creating new client profile...\n")
    
    client = Client.objects.create(
        user=client_user,
        company_name='Test Company Pvt Ltd',
        business_type='PVT_LTD',
        sector='IT_SOFTWARE',
        company_age=3,
        registration_number='U12345AB2020PTC123456',
        gst_number='27AABCU1234D1Z5',
        pan_number='AABCU1234D',
        contact_person_name=f"{client_user.first_name} {client_user.last_name}",
        contact_person_designation='Director',
        mobile_number='9876543210',
        email=client_user.email,
        registered_address='123, Test Street, Mumbai',
        city='Mumbai',
        state='Maharashtra',
        pincode='400001',
        annual_turnover=5000000.00,
        employee_count=15,
        assigned_sales=sales_user,
        created_by=sales_user if sales_user else None,
        client_status='ACTIVE'
    )
    
    print(f"✅ Created client profile: {client.company_name}")
    print(f"   Company Name: {client.company_name}")
    print(f"   Business Type: {client.business_type}")
    print(f"   Sector: {client.sector}")
    print(f"   Contact: {client.contact_person_name}")
    print(f"   Mobile: {client.mobile_number}")
    print(f"   Email: {client.email}")
    print(f"   City: {client.city}, {client.state}")
    print(f"   Status: {client.client_status}")
    if sales_user:
        print(f"   Assigned to: {sales_user.first_name} {sales_user.last_name}")
    
    print(f"\n🎯 Client can now login with:")
    print(f"   Email: {client_user.email}")
    print(f"   Password: Client@123")
    print(f"   Dashboard: http://127.0.0.1:8000/tracking/dashboard/")
    print(f"\n✅ Setup complete!")

if __name__ == '__main__':
    setup_client_profile()
